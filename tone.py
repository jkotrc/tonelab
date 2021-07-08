import numpy as np
from typing import Protocol

class ToneGenerator(Protocol):
    @staticmethod
    def sine_wave(frequency):
        return lambda x: np.sin(2*np.pi*frequency*x)

    def __call__(self, x: float) -> float:
        return self(x)


class Tone:
    def __init__(self, frequency, generator: ToneGenerator=None, samplerate=44100): #samplerate = samples per second
        self.frequency=frequency
        if generator is None:
            generator=ToneGenerator.sine_wave(self.frequency)
        if (generator(0) != generator(1/self.frequency)):
            raise ValueError(f"Function not periodic over [{0},{1/self.frequency}]!")

    def get_tonespace(self):
        return np.linspace(0,1/self.frequency, int(np.ceil(self.samplerate/self.frequency)))

    def evaluate(self):
        return generator(get_tonespace())
