from dataclasses import dataclass
from os import path

import matplotlib.pyplot as plt
import numpy as np

import constants
from audio.processing import Filter, Vocoder
from audio.recording import AudioSignal


@dataclass
class Parameters:
    num_filters: int = 0
    input_path: str = None
    output_path: str = None
    compression_level: float = 0.0


def process(params: Parameters):
    if path.exists(params.input_path):
        audio = AudioSignal.from_wav(params.input_path)
    else:
        return

    log_range = np.logspace(
        0, np.log10(audio.spectrum().sample_rate / 2), 2 * params.num_filters
    )
    filters = [
        Filter(log_range[2 * n + 1], (log_range[2 * n + 1] - log_range[2 * n]) / 2)
        for n in range(0, params.num_filters)
    ]

    v = Vocoder()
    compressed_spectrum, _, params.compression_level = v.modulate(audio, filters)
    inverted = compressed_spectrum.invert()
    inverted.save(params.output_path)

    # size of plots to be generated, in inches
    ploty = 6
    plotx = 4

    plt.figure(figsize=(ploty, plotx), dpi=80)
    audio.plot()
    plt.savefig(constants.INPUT_SIGNAL)

    plt.figure(figsize=(ploty, plotx), dpi=80)
    audio.spectrum().plot()
    plt.savefig(constants.INPUT_SPECTRUM)

    plt.figure(figsize=(ploty, plotx), dpi=80)
    inverted.plot()
    plt.savefig(constants.OUTPUT_SIGNAL)

    plt.figure(figsize=(ploty, plotx), dpi=80)
    compressed_spectrum.plot()
    plt.savefig(constants.OUTPUT_SPECTRUM)

    plt.close("all")


# play input audio
def play_in_audio(params: Parameters):
    if path.exists(params.input_path):
        audio = AudioSignal.from_wav(params.input_path)
        audio.play()


# play output audio
def play_out_audio(params: Parameters):
    if path.exists(params.output_path):
        audio = AudioSignal.from_wav(params.output_path)
        audio.play()
