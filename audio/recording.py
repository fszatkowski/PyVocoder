from dataclasses import dataclass

import numpy as np
import seaborn as sns
import sounddevice as sd
import soundfile as sf
from matplotlib import pyplot as plt
from scipy.fftpack import irfft, rfft


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
        if not input_path.endswith(".wav"):
            raise ValueError(f"File has to be in wav format: {input_path}")
        data, sample_rate = sf.read(input_path, dtype="float32", always_2d=True)
        duration = data.shape[0] / sample_rate
        return AudioSignal(data, sample_rate, duration, input_path)

    @staticmethod
    def from_mp3(input_path: str) -> "AudioSignal":
        # TODO check if loading works for mp3
        if not input_path.endswith(".mp3"):
            raise ValueError(f"File has to be in mp3 format: {input_path}")
        data, sample_rate = sf.read(input_path, dtype="float32", always_2d=True)
        duration = data.shape[0] / sample_rate
        return AudioSignal(data, sample_rate, duration, input_path)

    def stereo_to_mono(self) -> np.array:
        """ convert stereo signal to mono for audio processing"""
        if len(self.data.shape) == 2:
            return np.sum(self.data, axis=-1) / 2.0
        else:
            return self.data

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
        x = np.arange(0, self.duration, step * 1 / self.sample_rate)
        dims = len(self.data.shape)
        if dims == 2:
            y = self.stereo_to_mono()
        elif dims == 1:
            y = self.data
        else:
            raise AttributeError(f"Data has incorrect number of dimensions: {dims}")
        y = y[::step]
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
        # TODO technically we should use abs but it might break inverting
        #  so abs is used only for plotting
        """
        create spectrum from audio signal
        right fft is used (computes only positive values since fft is simetric)
        due to this, max_frequency is set to 0.5 * audio frequency
        """
        spectrum: np.array = rfft(audio.stereo_to_mono())
        return SpectralSignal(spectrum, audio.sample_rate / 2.0)

    def plot(self, step: int = 25):
        if self.data is None:
            raise AttributeError("AudioRecord is uninitialized.")
        x = np.arange(
            0, self.max_frequency, step * self.max_frequency / self.data.shape[0]
        )
        y = abs(self.data[::step])
        sns.lineplot(x=x, y=y)
        plt.show()

    def invert(self) -> AudioSignal:
        """
        when transforming audio to spectral signal, max_frequency is 0.5*audio sampling frequency
        so inverted signal audio frequency has to be set as twice max_frequency
        """
        inverse_fft = irfft(self.data)
        freq = 2 * self.max_frequency
        duration = inverse_fft.shape[0] / freq
        return AudioSignal(inverse_fft, freq, duration)


if __name__ == "__main__":
    test_record = AudioSignal.from_wav("../data/1.wav")
    spect = test_record.spectrum()
    ispect = spect.invert()
    diff = ispect.data - test_record.stereo_to_mono()
    assert np.all(diff < 1e-6)
