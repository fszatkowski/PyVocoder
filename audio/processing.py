from audio.recording import AudioSignal, STFTSignal
from dataclasses import dataclass
import numpy as np
from typing import *


@dataclass
class Filter:
    frequency: float
    bandwidth: float


@dataclass
class CompressedBandwidth:
    """ This is part of the frequency spectrum covered by filter in compressed form """
    f_min_idx: int
    f_max_idx: int
    amplitude: np.array


class Vocoder:
    filters: List[Filter] = []

    def __init__(self, filters):
        self.filters = filters

    def add_filter(self, frequency: int, width: int):
        self.filters.append(Filter(frequency, width))

    def remove_filter(self, f: Filter):
        self.filters.remove(f)

    def modulate(
        self, audio: AudioSignal, n_samples_per_window: int = None
    ) -> Tuple[STFTSignal, List[CompressedBandwidth]]:
        # compute compress bandwidth for each filter
        stft = audio.spectrum(n_samples_per_window)
        discrete_frequencies = stft.f
        compressed = []

        for f in self.filters:
            filtered_frequencies = discrete_frequencies[
                    (discrete_frequencies >= (f.frequency - f.bandwidth))
                    & (discrete_frequencies <= (f.frequency + f.bandwidth))
                ]

            if filtered_frequencies.size != 0:
                min_f_idx = np.argwhere(discrete_frequencies == filtered_frequencies[0])[0,0]
                max_f_idx = np.argwhere(discrete_frequencies == filtered_frequencies[-1])[0,0]
                if max_f_idx == min_f_idx:
                    bandwidth = stft.zxx[max_f_idx, :]
                    compressed.append(CompressedBandwidth(min_f_idx, max_f_idx, bandwidth))
                else:
                    bandwidth = stft.zxx[min_f_idx:max_f_idx, :]
                    max_amplitudes = np.argmax(abs(bandwidth), axis=0)

                    # idk how to do it smarter
                    amplitudes = bandwidth[0, :]
                    for i in range(0, max_amplitudes.shape[0]):
                        amplitudes[i] = bandwidth[max_amplitudes[i], i]
                    compressed.append(CompressedBandwidth(min_f_idx, max_f_idx, amplitudes))

        # use compressed bandwidths to recreate signal
        zxx = np.copy(stft.zxx)
        zxx[:,:] = 0
        for b in compressed:
            if b.f_min_idx == b.f_max_idx:
                zxx[b.f_max_idx, :] = b.amplitude
            else:
                zxx[b.f_min_idx : b.f_max_idx, :] = b.amplitude
        stft.zxx = zxx
        return stft, compressed

    def __str__(self):
        return " ".join(
            [f"f: {f.frequency}\tbandwidth: {f.bandwidth}\n" for f in self.filters]
        )
