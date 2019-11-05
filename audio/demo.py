from audio.processing import Vocoder, Filter
from audio.recording import AudioSignal
import numpy as np
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Args:
    scale: str = "log"
    num_filters: int = 100
    plot_resolution: int = 5


if __name__ == "__main__":
    #args = parse_args()
    args = Args("log", 500)

    audio = AudioSignal.from_wav("/home/filip/PycharmProjects/vocoder/data/1.wav")
    audio.plot(args.plot_resolution, log=True)
    audio_spectrum = audio.spectrum()
    audio_spectrum.plot(args.plot_resolution, log=True)

    num_filters = args.num_filters
    if args.scale == "log":
        log_range = np.logspace(0, np.log10(audio_spectrum.max_frequency), 2 * args.num_filters)
        filters = (
            [Filter(log_range[2 * n + 1], (log_range[2 * n + 1] - log_range[2 * n]) / 2) for n in
             range(0, args.num_filters)]
        )
    else:
        raise ValueError

    print("Modulating...")
    start = datetime.now()
    vocoder = Vocoder(filters)
    modulated_audio = vocoder.modulate(audio)
    print(f"Modulated audio file in {datetime.now() - start}")
    # modulated_audio.play()
    modulated_audio.plot(args.plot_resolution, log=True)
    modulated_audio.spectrum().plot(args.plot_resolution, log=True)
