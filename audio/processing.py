from audio.recording import AudioSignal, SpectralSignal
from dataclasses import dataclass
import numpy as np
from typing import *

# TODO - fix log plotting


@dataclass
class Filter:
    # TODO right now filter works by setting values outside of <frequency - bandwidth/2, frequency + bandwidth/2> to 0
    #  not sure if it's really correct
    frequency: float
    bandwidth: float

    def filter(self, signal: AudioSignal) -> SpectralSignal:
        spectrum = SpectralSignal.from_audio(signal)
        step = spectrum.data.shape[0] / spectrum.max_frequency
        filter_mask = frequency_bandwidth_mask(
            self.frequency, self.bandwidth, spectrum.data.shape[0], step
        )
        spectrum.data[~filter_mask] = 0.0
        return spectrum


@dataclass
class FilteredBandwidth:
    """ This is part of the frequency spectrum covered by filter in compressed form """

    frequency: float
    bandwidth: float
    amplitude: float

    def noise_modulate(self, sample_rate: float, n_samples: float) -> SpectralSignal:
        """ White noise = constant spectrum
        modulating noise with amplitude in audio domain
        equals setting amplitudes in given range of frequencies to the value of this amplitude in frequency domain"""
        signal = np.zeros(int(n_samples))
        step = sample_rate / n_samples
        mask = frequency_bandwidth_mask(
            self.frequency, self.bandwidth, int(n_samples), step
        )
        signal[mask] = self.amplitude
        return SpectralSignal(signal, sample_rate)


class Vocoder:
    filters: List[Filter] = []

    def __init__(self, filters):
        self.filters = filters

    def add_filter(self, frequency: int, width: int):
        self.filters.append(Filter(frequency, width))

    def remove_filter(self, f: Filter):
        self.filters.remove(f)

    def modulate(self, audio: AudioSignal) -> AudioSignal:
        # compute filtered signals
        compressed_signals = []

        filtered_signal = None
        for f in self.filters:
            filtered_signal = f.filter(audio)
            max_amplitude = np.max(filtered_signal.data)
            compressed_signal = FilteredBandwidth(
                f.frequency, f.bandwidth, max_amplitude
            )
            compressed_signals.append(compressed_signal)

        # create new signal by modulating noise with filter amplitudes and adding each other
        n_samples = filtered_signal.data.shape[0]
        sample_rate = filtered_signal.max_frequency
        modulated_noises = [
            cs.noise_modulate(sample_rate, n_samples).data for cs in compressed_signals
        ]
        stacked_signals = np.stack(modulated_noises, axis=-1)
        stacked_signals_sum = np.sum(stacked_signals, axis=-1)
        combined_signal = SpectralSignal(stacked_signals_sum, sample_rate)

        return combined_signal.invert()

    def __str__(self):
        return " ".join(
            [f"f: {f.frequency}\tbandwidth: {f.bandwidth}\n" for f in self.filters]
        )


def frequency_bandwidth_mask(
    frequency: float, bandwidth: float, n_values: int, step: float
) -> np.array:
    min_idx = (frequency - bandwidth / 2) / step
    max_idx = (frequency + bandwidth / 2) / step
    indices = np.array([i for i in range(0, int(n_values))])
    return (indices > min_idx) * (indices < max_idx)
