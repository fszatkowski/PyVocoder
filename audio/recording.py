from dataclasses import dataclass

import numpy as np
import seaborn as sns
import sounddevice as sd
import soundfile as sf
from matplotlib import pyplot as plt
from scipy.signal import stft, istft


@dataclass
class AudioSignal:
    data: np.array
    sample_rate: float
    duration: float
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
        sd.stop()
        # for some reason sd doesnt work with mono so signal is copied
        sd.play(self.data, self.sample_rate)
        sd.wait()

    def save(self, output_filename: str, log: bool = False):
        sf.write(output_filename, self.data, int(self.sample_rate))
        sd.wait()

    def plot(self, step: int = 25):
        dims = len(self.data.shape)
        if dims == 2:
            y = self.stereo_to_mono()
        elif dims == 1:
            y = self.data
        else:
            raise AttributeError(f"Data has incorrect number of dimensions: {dims}")
        y = y[::step]

        x = np.arange(0, y.shape[0] * step * 1/self.sample_rate, step*1/self.sample_rate)
        sns.lineplot(x=x, y=y)
        plt.show()

    def spectrum(self, n_samples_per_segment: int = None) -> "STFTSignal":
        return STFTSignal.from_audio(self, n_samples_per_segment)


@dataclass
class STFTSignal:
    zxx: np.array
    f: np.array
    t: np.array
    sample_rate: float

    @staticmethod
    def from_audio(audio: AudioSignal, n_samples_per_segment: int = None) -> "STFTSignal":
        # TODO technically we should use abs but it might break inverting
        #  so abs is used only for plotting
        """
        computes stft from audio signal with given number of samples in window
        """
        if n_samples_per_segment is None:
            n_samples_per_segment = 256
        f, t, zxx = stft(audio.stereo_to_mono(), nperseg=n_samples_per_segment, fs=audio.sample_rate)
        return STFTSignal(zxx, f, t, audio.sample_rate)

    def plot(self, f_step: int = 1, t_step: int = 1):
        z = np.abs(self.zxx[::f_step, ::t_step])

        t = self.t[::t_step]
        f = self.f[::f_step]

        plt.pcolormesh(t, f, z, vmin=0, vmax=np.max(z))
        plt.title('STFT Magnitude')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

    def invert(self) -> AudioSignal:
        t, inverse_stft = istft(self.zxx, self.sample_rate)
        # convert to stereo
        stereo = np.column_stack((inverse_stft, inverse_stft))
        return AudioSignal(stereo, self.sample_rate, t[-1])
