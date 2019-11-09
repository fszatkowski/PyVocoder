from audio.processing import Vocoder, Filter
from audio.recording import AudioSignal
import numpy as np
from dataclasses import dataclass


@dataclass
class Args:
    num_filters: int = 100
    plot_resolution: int = 5


if __name__ == "__main__":
    # args = parse_args()
    args = Args(1000, 25)

#    audio = AudioSignal.from_wav("/home/filip/PycharmProjects/vocoder/data/1.wav")

    print("Record 3s audio.")
    audio = AudioSignal.from_microphone(44100, 3)
    print("Playing back")
    audio.play()
    audio.plot(args.plot_resolution)
    audio_spectrum = audio.spectrum()
    audio_spectrum.plot()
    print("Thanks.")

    num_filters = args.num_filters
    log_range = np.logspace(
        0, np.log10(audio_spectrum.sample_rate / 2), 2 * args.num_filters
    )
    filters = [
        Filter(log_range[2 * n + 1], (log_range[2 * n + 1] - log_range[2 * n]) / 2)
        for n in range(0, args.num_filters)
    ]

    print("Modulating...")
    v = Vocoder(filters)
    compressed_spectrum, _ = v.modulate(audio)
    compressed_spectrum.plot()

    print("Playing coded version.")
    inverted = compressed_spectrum.invert()
    inverted.plot(args.plot_resolution)
    print(inverted.data.shape)
    inverted.play()
