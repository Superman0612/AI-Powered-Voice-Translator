import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, AlertCircle } from 'lucide-react';

interface MicrophoneRecorderProps {
  onRecordingComplete: (blob: Blob, audioUrl: string) => void;
  disabled?: boolean;
}

export const MicrophoneRecorder: React.FC<MicrophoneRecorderProps> = ({
  onRecordingComplete,
  disabled = false
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [permissionError, setPermissionError] = useState<string | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<any>(null);

  useEffect(() => {
    return () => {
      // Cleanup tracks on unmount
      if (timerRef.current) clearInterval(timerRef.current);
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const startRecording = async () => {
    setPermissionError(null);
    chunksRef.current = [];
    setRecordingTime(0);

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Your browser does not support microphone audio capture.");
      }

      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true
        } 
      });
      streamRef.current = stream;

      // Check supported MIME types in order of preference
      let mimeType = 'audio/webm';
      if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
        mimeType = 'audio/webm;codecs=opus';
      } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
        mimeType = 'audio/mp4';
      } else if (MediaRecorder.isTypeSupported('audio/ogg')) {
        mimeType = 'audio/ogg';
      }

      const recorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: mimeType });
        const audioUrl = URL.createObjectURL(audioBlob);
        onRecordingComplete(audioBlob, audioUrl);
        // Release hardware mic track
        stream.getTracks().forEach((track) => track.stop());
      };

      recorder.start(250); // collect 250ms chunks
      setIsRecording(true);

      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);

    } catch (err: any) {
      console.error("Microphone capture failed:", err);
      let errorMsg = "Microphone access denied or audio device not found.";
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        errorMsg = "Microphone permission was denied. Please allow microphone access in your browser settings.";
      }
      setPermissionError(errorMsg);
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
      {permissionError && (
        <div className="w-full mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{permissionError}</span>
        </div>
      )}

      {/* Main Mic Button with Pulsing Wave Effect */}
      <div className="relative flex items-center justify-center my-2">
        {isRecording && (
          <>
            <span className="animate-ping absolute inline-flex h-24 w-24 rounded-full bg-rose-500 opacity-40"></span>
            <span className="animate-pulse absolute inline-flex h-20 w-20 rounded-full bg-rose-500/30"></span>
          </>
        )}

        <button
          type="button"
          onClick={isRecording ? stopRecording : startRecording}
          disabled={disabled}
          className={`relative z-10 w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300 shadow-xl ${
            isRecording
              ? 'bg-rose-600 hover:bg-rose-500 text-white scale-110 shadow-rose-600/40'
              : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30 hover:scale-105'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          title={isRecording ? "Stop Recording" : "Start Voice Recording"}
        >
          {isRecording ? (
            <Square className="w-6 h-6 fill-current animate-pulse" />
          ) : (
            <Mic className="w-7 h-7" />
          )}
        </button>
      </div>

      {/* Recording Status & Timer */}
      <div className="mt-4 text-center">
        {isRecording ? (
          <div className="flex flex-col items-center gap-1">
            <div className="flex items-center gap-2 text-rose-400 font-mono text-base font-bold">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping" />
              <span>Recording: {formatTimer(recordingTime)}</span>
            </div>
            <p className="text-xs text-slate-400">Speak clearly in your chosen Indian language. Tap square to finish.</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-0.5">
            <span className="text-sm font-semibold text-slate-200">Tap microphone to speak</span>
            <span className="text-xs text-slate-400">Supports Hindi, Tamil, Telugu, Gujarati, Marathi, etc.</span>
          </div>
        )}
      </div>
    </div>
  );
};
