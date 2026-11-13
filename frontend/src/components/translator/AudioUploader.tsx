import React, { useRef, useState } from 'react';
import { UploadCloud, FileAudio, X, AlertCircle } from 'lucide-react';
import { AudioPlayer } from '../common/AudioPlayer';

interface AudioUploaderProps {
  onFileSelected: (file: File) => void;
  onClear: () => void;
  selectedFile: File | null;
  previewUrl: string | null;
  disabled?: boolean;
}

export const AudioUploader: React.FC<AudioUploaderProps> = ({
  onFileSelected,
  onClear,
  selectedFile,
  previewUrl,
  disabled = false
}) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);

  const allowedExtensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a'];

  const validateAndHandle = (file: File) => {
    setValidationError(null);
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!allowedExtensions.includes(ext)) {
      setValidationError(`Unsupported audio format '${ext}'. Allowed: WAV, MP3, OGG, FLAC, M4A.`);
      return;
    }

    const maxSizeMB = 25;
    if (file.size > maxSizeMB * 1024 * 1024) {
      setValidationError(`File exceeds maximum size limit of ${maxSizeMB}MB.`);
      return;
    }

    onFileSelected(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndHandle(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndHandle(e.target.files[0]);
    }
  };

  return (
    <div className="space-y-3">
      {validationError && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{validationError}</span>
        </div>
      )}

      {!selectedFile ? (
        <div
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          onClick={() => !disabled && fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all ${
            isDragging
              ? 'border-indigo-500 bg-indigo-500/10 scale-[0.99]'
              : 'border-slate-800 bg-slate-900/40 hover:bg-slate-900/80 hover:border-slate-700'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".wav,.mp3,.ogg,.flac,.m4a,audio/*"
            onChange={handleChange}
            disabled={disabled}
            className="hidden"
          />
          <div className="flex flex-col items-center gap-2">
            <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center text-indigo-400">
              <UploadCloud className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-200">
                Click to upload audio or drag and drop
              </p>
              <p className="text-xs text-slate-400 mt-1">
                WAV, MP3, FLAC, OGG up to 25MB (16kHz recommended)
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3 truncate">
              <div className="w-9 h-9 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0">
                <FileAudio className="w-5 h-5" />
              </div>
              <div className="truncate">
                <p className="text-xs font-semibold text-slate-200 truncate">{selectedFile.name}</p>
                <p className="text-[11px] text-slate-400">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Ready for ASR pipeline
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={onClear}
              disabled={disabled}
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition-colors"
              title="Remove audio"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {previewUrl && (
            <AudioPlayer src={previewUrl} title="Input Audio Preview" className="bg-slate-950 border-slate-850" />
          )}
        </div>
      )}
    </div>
  );
};

