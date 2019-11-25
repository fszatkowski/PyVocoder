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
    @staticmethod
    def modulate(
        audio: AudioSignal, filters: Sequence[Filter], n_samples_per_window: int = None
    ) -> Tuple[STFTSignal, List[CompressedBandwidth], float]:
        # compute compress bandwidth for each filter
        stft = audio.spectrum(n_samples_per_window)
        stft_frequencies = stft.f
        modulated_bandwidths = []

        for f in filters:
            # get the frequencies corresponding to filter's bandwidth
            mask = (stft_frequencies >= (f.frequency - f.bandwidth)) & (
                stft_frequencies <= (f.frequency + f.bandwidth)
            )
            filtered_frequencies = np.copy(stft_frequencies[mask])

            # proceed only if given bandwidth matches any discrete sample
            if filtered_frequencies.size != 0:
                min_f_idx, max_f_idx = _find_min_max_indices(
                    stft_frequencies, filtered_frequencies
                )
                bandwidth = np.copy(stft.zxx[min_f_idx:max_f_idx, :])
                if max_f_idx == min_f_idx:
                    # if max and min idx are the same, take only one sample for each time window
                    modulated_bandwidths.append(
                        CompressedBandwidth(min_f_idx, max_f_idx, bandwidth)
                    )
                else:
                    # we need to find and pass maximum values from bandwidth STFT
                    # idk how to do it smarter - np.max behaves weirdly with complex numbers
                    # so the code below is not really optimal and could be improved
                    max_amplitudes = np.argmax(abs(bandwidth), axis=0)
                    # amplitudes = np.zeros((1, bandwidth.shape[1]))
                    amplitudes = np.copy(bandwidth[0, :])
                    for i in range(0, max_amplitudes.shape[0]):
                        amplitudes[i] = bandwidth[max_amplitudes[i], i]
                    modulated_bandwidths.append(
                        CompressedBandwidth(min_f_idx, max_f_idx, amplitudes)
                    )

        # use compressed bandwidths to recreate signal
        # modulated signal is non zero only for bandwidths covered by filters
        # for bandwidths covered by filters we set constant amplitude which should be equal to noise modulating
        zxx = np.copy(stft.zxx)
        zxx[:, :] = 0
        for b in modulated_bandwidths:
            zxx[b.f_min_idx : b.f_max_idx, :] = b.amplitude

        stft.zxx = zxx

        # compute compression level - instead of f * t samples we send (m + 2) numbers for each filter
        # m - number of samples for each amplitude, add +2 since we have to also send min and max index
        compression_level = (audio.data.shape[0] * audio.data.shape[1]) / (
            len(modulated_bandwidths) * (modulated_bandwidths[0].amplitude.shape[0] + 2)
        )
        return stft, modulated_bandwidths, compression_level


def _find_min_max_indices(
    discrete_frequencies: np.array, filtered_frequencies: np.array
) -> Tuple[int, int]:
    # this should return first and last index corresponding to the bandwidth we need
    # argwhere returns indices which match given condition, those indices are stored in a weird way as 2d array each
    min_f_idx = np.argwhere(discrete_frequencies == filtered_frequencies[0])[0, 0]
    max_f_idx = np.argwhere(discrete_frequencies == filtered_frequencies[-1])[0, 0]
    # since numpy indexing is not inclusive for the last element, add + 1 to last index to allow easier slicing
    # TODO if something doesn't work the bug may be here:D
    return min_f_idx, max_f_idx + 1
