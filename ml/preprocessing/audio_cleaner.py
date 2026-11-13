"""
Audio Preprocessing & Noise Experimentation Utilities
Implements additive Gaussian noise, Signal-to-Noise Ratio (SNR) computation,
and spectral gating benchmarks.
"""

import numpy as np

def calculate_snr_db(signal: np.ndarray, noise: np.ndarray) -> float:
    """Calculates Signal-to-Noise Ratio in decibels."""
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    if noise_power < 1e-12:
        return 100.0  # Virtually infinite SNR
    snr = 10 * np.log10(signal_power / noise_power)
    return round(float(snr), 2)

def inject_gaussian_noise(signal: np.ndarray, target_snr_db: float = 15.0) -> np.ndarray:
    """Injects additive white Gaussian noise to simulate noisy acoustic environments."""
    signal_power = np.mean(signal ** 2)
    if signal_power < 1e-12:
        return signal

    required_noise_power = signal_power / (10 ** (target_snr_db / 10))
    noise = np.random.normal(0, np.sqrt(required_noise_power), size=signal.shape)
    noisy_signal = signal + noise
    # Prevent clipping
    max_val = np.max(np.abs(noisy_signal))
    if max_val > 1.0:
        noisy_signal = noisy_signal / max_val
    return noisy_signal.astype(np.float32)

