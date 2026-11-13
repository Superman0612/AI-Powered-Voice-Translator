"""
Audio Digital Signal Processing (DSP) & Preprocessing Engine for ASR
Handles format validation, channel reduction, 16kHz resampling,
peak normalization, silence detection, and noise reduction.
"""

import os
import logging
from typing import Tuple, Dict, Any, Optional
import numpy as np
import scipy.signal
import soundfile as sf
from app.core.config import settings

logger = logging.getLogger("bhashaai.services.audio_dsp")

class AudioProcessingError(Exception):
    pass

class AudioProcessor:
    @staticmethod
    def validate_file(file_path: str) -> Dict[str, Any]:
        """Validates existence, extension, and non-empty size."""
        if not os.path.exists(file_path):
            raise AudioProcessingError(f"Audio file not found: {file_path}")

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise AudioProcessingError("Uploaded audio file is empty (0 bytes).")

        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise AudioProcessingError(
                f"Audio file exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit ({round(file_size/(1024*1024), 2)}MB)."
            )

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
            raise AudioProcessingError(
                f"Unsupported audio format '{ext}'. Supported: {', '.join(settings.ALLOWED_AUDIO_EXTENSIONS)}"
            )

        return {
            "file_size": file_size,
            "extension": ext,
            "valid": True
        }

    @staticmethod
    def load_audio(file_path: str) -> Tuple[np.ndarray, int]:
        """Loads audio file into float32 numpy array and sample rate."""
        AudioProcessor.validate_file(file_path)
        try:
            data, sample_rate = sf.read(file_path, dtype='float32')
            return data, sample_rate
        except Exception as e:
            logger.error(f"Failed to read audio file via soundfile: {e}")
            raise AudioProcessingError(f"Corrupt or unreadable audio format: {str(e)}")

    @staticmethod
    def to_mono(audio: np.ndarray) -> np.ndarray:
        """Converts multi-channel audio to single-channel mono."""
        if audio.ndim == 1:
            return audio
        elif audio.ndim == 2:
            return np.mean(audio, axis=1)
        else:
            raise AudioProcessingError(f"Unsupported audio shape: {audio.shape}")

    @staticmethod
    def resample(audio: np.ndarray, orig_sr: int, target_sr: int = 16000) -> np.ndarray:
        """Resamples audio array to target sample rate (default 16kHz for Whisper)."""
        if orig_sr == target_sr:
            return audio

        num_target_samples = int(round(len(audio) * float(target_sr) / orig_sr))
        if num_target_samples == 0:
            return np.array([], dtype=np.float32)

        resampled = scipy.signal.resample(audio, num_target_samples)
        return resampled.astype(np.float32)

    @staticmethod
    def normalize_amplitude(audio: np.ndarray, target_peak: float = 0.95) -> np.ndarray:
        """Peak-normalizes the signal to prevent clipping and improve SNR."""
        max_val = np.max(np.abs(audio))
        if max_val > 1e-6:
            return audio * (target_peak / max_val)
        return audio

    @staticmethod
    def detect_silence(audio: np.ndarray, sr: int = 16000, threshold_db: float = -40.0) -> Dict[str, Any]:
        """
        Detects silent regions and trims leading/trailing silence.
        Calculates Root-Mean-Square (RMS) energy.
        """
        if len(audio) == 0:
            return {"is_silent": True, "trimmed_audio": audio, "silence_ratio": 1.0}

        # Frame-based energy computation (25ms window, 10ms hop)
        frame_len = int(sr * 0.025)
        hop_len = int(sr * 0.010)
        
        frames = []
        for i in range(0, len(audio) - frame_len, hop_len):
            frame = audio[i:i + frame_len]
            rms = np.sqrt(np.mean(frame ** 2) + 1e-12)
            frames.append(rms)

        if not frames:
            return {"is_silent": False, "trimmed_audio": audio, "silence_ratio": 0.0}

        frames = np.array(frames)
        max_rms = np.max(frames)
        if max_rms <= 1e-5:
            return {"is_silent": True, "trimmed_audio": audio, "silence_ratio": 1.0}

        db_frames = 20 * np.log10(frames / max_rms + 1e-12)
        non_silent_idx = np.where(db_frames > threshold_db)[0]

        if len(non_silent_idx) == 0:
            return {"is_silent": True, "trimmed_audio": audio, "silence_ratio": 1.0}

        start_sample = non_silent_idx[0] * hop_len
        end_sample = min(len(audio), (non_silent_idx[-1] + 1) * hop_len + frame_len)
        trimmed = audio[start_sample:end_sample]
        silence_ratio = 1.0 - (len(trimmed) / len(audio))

        return {
            "is_silent": False,
            "trimmed_audio": trimmed,
            "silence_ratio": round(silence_ratio, 3),
            "start_sample": start_sample,
            "end_sample": end_sample
        }

    @staticmethod
    def apply_spectral_noise_reduction(audio: np.ndarray, sr: int = 16000) -> np.ndarray:
        """
        Spectral gating noise attenuation experiment.
        Estimates stationary background noise from the first 100ms and subtracts spectral floor.
        """
        if len(audio) < int(sr * 0.2):
            return audio

        # Compute STFT
        f, t, Zxx = scipy.signal.stft(audio, fs=sr, nperseg=512)
        magnitude = np.abs(Zxx)
        phase = np.angle(Zxx)

        # Estimate noise profile from initial frames
        noise_frames = min(10, magnitude.shape[1] // 5)
        noise_profile = np.mean(magnitude[:, :noise_frames], axis=1, keepdims=True)

        # Spectral subtraction with oversubtraction factor alpha and spectral floor beta
        alpha = 1.5
        beta = 0.05
        subtracted = magnitude - alpha * noise_profile
        subtracted = np.maximum(subtracted, beta * magnitude)

        # Invert STFT
        _, clean_audio = scipy.signal.istft(subtracted * np.exp(1j * phase), fs=sr)
        return clean_audio.astype(np.float32)

    @classmethod
    def preprocess_pipeline(cls, file_path: str, apply_denoise: bool = False) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Complete Audio DSP Pipeline:
        Raw file -> Validation -> Mono -> 16kHz Resample -> Silence Detection -> Normalization -> (Optional Denoise)
        """
        raw_data, orig_sr = cls.load_audio(file_path)
        mono_data = cls.to_mono(raw_data)
        resampled_data = cls.resample(mono_data, orig_sr, target_sr=settings.SAMPLE_RATE)
        
        silence_info = cls.detect_silence(resampled_data, sr=settings.SAMPLE_RATE)
        active_audio = silence_info["trimmed_audio"]
        
        if apply_denoise and not silence_info["is_silent"]:
            active_audio = cls.apply_spectral_noise_reduction(active_audio, sr=settings.SAMPLE_RATE)
            
        normalized_audio = cls.normalize_amplitude(active_audio)
        duration_sec = len(normalized_audio) / float(settings.SAMPLE_RATE)

        meta = {
            "original_sample_rate": orig_sr,
            "target_sample_rate": settings.SAMPLE_RATE,
            "original_channels": 2 if raw_data.ndim > 1 else 1,
            "duration_seconds": round(duration_sec, 2),
            "is_silent": silence_info["is_silent"],
            "silence_ratio": silence_info.get("silence_ratio", 0.0)
        }

        return normalized_audio, meta
