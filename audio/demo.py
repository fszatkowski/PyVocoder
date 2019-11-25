from audio.processing import Vocoder, Filter
from audio.recording import AudioSignal
import numpy as np
from dataclasses import dataclass
import os
import matplotlib.pyplot as plt


@dataclass
class Args:
    num_filters: int = 100
    plot_resolution: int = 25


if __name__ == "__main__":
    # args = parse_args()
    args = Args(num_filters=3)

    # print(os.getcwd())
    audio = AudioSignal.from_wav("../data/2.wav")

    # print("Record 3s audio.")
    # audio = AudioSignal.from_microphone(44100, 3)
    # print("Playing back")
    audio.play()
    plt.figure()
    plot = audio.plot()
    plt.savefig("ASdasdas2")

    audio_spectrum = audio.spectrum()
    plt.figure()
    plot = audio_spectrum.plot()
    plt.savefig("ASdasdas")
    #    print("Thanks.")

    num_filters = args.num_filters
    log_range = np.logspace(
        0, np.log10(audio_spectrum.sample_rate / 2), 2 * args.num_filters
    )
    filters = [
        Filter(log_range[2 * n + 1], (log_range[2 * n + 1] - log_range[2 * n]) / 2)
        for n in range(0, args.num_filters)
    ]

    print("Modulating...")
    v = Vocoder()
    compressed_spectrum, _, compression_level = v.modulate(audio, filters)
    print(f"compression level: {compression_level}\r\n")
    compressed_spectrum.plot()

    print("Playing coded version.")
    inverted = compressed_spectrum.invert()
    inverted.plot(args.plot_resolution)
    print(inverted.data.shape)
    inverted.play()
