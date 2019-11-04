from audio.processing import Vocoder, Filter
from audio.recording import AudioSignal

if __name__ == "__main__":
    filters = [
        Filter(n, 0.1*n) for n in range(0, 44100, 100)
    ]

    vocoder = Vocoder(filters)
    print("Recording 3s audio.\n")
    audio = AudioSignal.from_microphone(44100, 1)
    audio.plot(100)
    modulated_audio = vocoder.modulate(audio)
    print("Playing back modulated audio.\n")
    modulated_audio.play()
    modulated_audio.plot(100)
    modulated_audio.spectrum().plot(100)
