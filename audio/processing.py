from dataclasses import dataclass
from typing import *

import numpy

from audio.recording import AudioRecord


# TODO - UNIT TESTS!


@dataclass
class Filter:
    frequency: float = 0
    amplitude: int = 0


@dataclass
class FilteredAudioRecord(AudioRecord):
    filters: List[Filter] = None


class Vocoder:
    filters: List[Filter] = []
    records: List[FilteredAudioRecord] = []

    # TODO how tf it works
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def add_filter(self):
        pass

    def remove_filter(self):
        pass

    def modulate(self, recording: AudioRecord) -> FilteredAudioRecord:
        pass

    def __str__(self):
        return " ".join(
            [
                f"f: {filter.frequency}\tamplitude: {filter.amplitude}\n"
                for filter in self.filters
            ]
        )
