from audio.recording import AudioSignal


class Vocoder:
    filters = []

    # TODO how tf it works
    def __init__(self, filters):
        self.filters = filters

    def add_filter(self):
        pass

    def remove_filter(self):
        pass

    def modulate(self, recording: AudioSignal):
        pass

    def __str__(self):
        return " ".join(
            [
                f"f: {filter.frequency}\tamplitude: {filter.amplitude}\n"
                for filter in self.filters
            ]
        )
