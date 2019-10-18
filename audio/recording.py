from dataclasses import dataclass
from typing import *

import numpy as np

import sounddevice as sd
import soundfile as sf

# TODO - UNIT TESTS!


@dataclass
class RecordData:
    data: np.array = None
    sample_rate: int = None
    duration: float = None
    filename: str = None


class AudioRecord:
    _record: RecordData = None
    TAudioRecord = TypeVar("TAudioRecord", bound="AudioRecord")

    def __init__(self, record_data: RecordData):
        if record_data.data is None or record_data.sample_rate is None:
            raise ValueError
        if record_data.duration is None:
            record_data.duration = record_data.data.shape[0] / record_data.sample_rate
        self._record = record_data

    @staticmethod
    def from_microphone(sample_rate: int, duration: float) -> TAudioRecord:
        sd.stop()
        recording = sd.rec(
            int(duration * sample_rate), samplerate=sample_rate, channels=2
        )
        sd.wait()
        return AudioRecord(RecordData(recording, sample_rate, duration))

    @staticmethod
    def from_wav(input_path: str) -> TAudioRecord:
        # TODO check if path and extension are correct and throw ValueError if not
        data, sample_rate = sf.read(input_path, dtype="float32", always_2d=True)
        duration = data.shape[0] / sample_rate
        return AudioRecord(RecordData(data, sample_rate, duration, input_path))

    @staticmethod
    def from_mp3(input_path: str) -> TAudioRecord:
        # TODO check if path and extension are correct and throw ValueError if not
        #  also check if loading works for mp3
        data, sample_rate = sf.read(input_path, dtype="float32", always_2d=True)
        duration = data.shape[0] / sample_rate
        return AudioRecord(RecordData(data, sample_rate, duration, input_path))

    def play(self):
        if self._record is None:
            raise AttributeError("AudioRecord is uninitialized.")
        sd.stop()
        sd.play(self._record.data, self._record.sample_rate)
        sd.wait()

    def save(self, output_filename: str):
        if self._record is None:
            raise AttributeError("AudioRecord is uninitialized.")
        # TODO - maybe use process for it?
        sf.write(output_filename, self._record.data, self._record.sample_rate)
        sd.wait()


if __name__ == "__main__":
    print("Recording... (3s)")
    record1 = AudioRecord.from_microphone(44100, 3.0)
    print("Recording finished")
    record1.play()
    record1.save("../data/test.wav")

    print("Playing from saved recording.")
    record2 = AudioRecord.from_wav("../data/test.wav")
    record2.play()

    print("Playing from downloaded.")
    record3 = AudioRecord.from_wav("../data/1.wav")
    record3.play()
