from dataclasses import dataclass

from scipy.fftpack import rfft, irfft
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import sounddevice as sd
import soundfile as sf


@dataclass
class AudioSignal:
    data: np.array = None
    sample_rate: float = None
    duration: float = None
    filename: str = None

    @staticmethod
    def from_microphone(sample_rate: float, duration: float) -> "AudioSignal":
        sd.stop()
        recording = sd.rec(
            int(duration * sample_rate), samplerate=sample_rate, channels=2
        )
        sd.wait()
        return AudioSignal(recording, sample_rate, duration)

    @staticmethod
    def from_wav(input_path: str) -> "AudioSignal":
        # TODO check if path and extension are correct and throw ValueError if not
        data, sample_rate = sf.read(input_path, dtype="float32", always_2d=True)
        duration = data.shape[0] / sample_rate
        return AudioSignal(data, sample_rate, duration, input_path)

    @staticmethod
    def from_mp3(input_path: str) -> "AudioSignal":
        # TODO check if path and extension are correct and throw ValueError if not
        #  also check if loading works for mp3
        data, sample_rate = sf.read(input_path, dtype="float32", always_2d=True)
        duration = data.shape[0] / sample_rate
        return AudioSignal(data, sample_rate, duration, input_path)

    def stereo_to_mono(self) -> np.array:
        """ convert stereo signal to mono for audio processing"""
        return np.sum(self.data, axis=1)/2.0

    def play(self):
        if self.data is None:
            raise AttributeError("AudioRecord is uninitialized.")
        sd.stop()
        sd.play(self.data, self.sample_rate)
        sd.wait()

    def save(self, output_filename: str):
        if self.data is None:
            raise AttributeError("AudioRecord is uninitialized.")
        sf.write(output_filename, self.data, int(self.sample_rate))
        sd.wait()

    def plot(self, step: int = 25):
        if self.data is None:
            raise AttributeError("AudioRecord is uninitialized.")
        x = np.arange(0, self.duration, step*1/self.sample_rate)
        y = self.stereo_to_mono()[::step]
        print(x.shape, y.shape)
        sns.lineplot(x=x, y=y)
        plt.show()

    def spectrum(self) -> "SpectralSignal":
        return SpectralSignal.from_audio(self)


@dataclass
class SpectralSignal:
    data: np.array = None
    max_frequency: float = None

    @staticmethod
    def from_audio(audio: AudioSignal) -> "SpectralSignal":
        spectrum: np.array = np.abs(rfft(audio.stereo_to_mono()))
        return SpectralSignal(spectrum, audio.sample_rate/2)

    def plot(self, step: int = 25):
        if self.data is None:
            raise AttributeError("AudioRecord is uninitialized.")
        x = np.arange(0, self.max_frequency, step*self.max_frequency/self.data.shape[0])
        y = self.data[::step]
        sns.lineplot(x=x, y=y)
        plt.show()

    def inverse(self) -> AudioSignal:
        # TODO doesn't work yet :(

        inverse_fft = irfft(self.data)
        freq = 2*self.max_frequency
        return AudioSignal(inverse_fft, freq, inverse_fft.shape[0]/freq)


if __name__ == "__main__":
    # print("Recording... (3s)")
    # record1 = AudioRecord.from_microphone(44100, 3.0)
    # print("Recording finished")
    # record1.play()
    # record1.save("../data/test.wav")

    # print("Playing from saved recording.")
    # record2 = AudioRecord.from_wav("../data/test.wav")
    # record2.play()

    print("Playing from downloaded.")
    record3 = AudioSignal.from_wav("../data/1.wav")
    record3.plot(step=100)
    spect = record3.spectrum()
    spect.plot(100)
    ispect = spect.inverse()
    ispect.plot()
    # record3.play()
