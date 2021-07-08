import numpy as np
from typing import Protocol
import math

class ToneGenerator(Protocol):
    @staticmethod
    def sine_wave(frequency):
        return lambda x: np.sin(2*np.pi*frequency*x)

    def __call__(self, x: float) -> float:
        return self(x)


class Tone:
    def __init__(self, frequency, generator: ToneGenerator=None, samplerate=44100): #samplerate = samples per second
        self.samplerate=samplerate
        self.frequency=frequency
        if generator is None:
            generator=ToneGenerator.sine_wave(self.frequency)
        self.generator=generator
        if not math.isclose(generator(0),generator(1/self.frequency), rel_tol=1e-05, abs_tol=1e-10):
            raise ValueError(f"Function not periodic over [{0},{1/self.frequency}]!\n expected {generator(0)} == {generator(1/self.frequency)}")

    def __eq__(self, other):
        samefreq = (self.frequency == other.frequency)
        samevals = (self.evaluate() == other.evaluate()).all()
        return (samefreq and samevals)

    def get_tonespace(self):
        return np.linspace(0,1/self.frequency, int(np.ceil(self.samplerate/self.frequency)))

    def get_frequency(self):
        return self.frequency

    def get_samplerate(self):
        return self.samplerate

    def evaluate(self):
        return self.generator(self.get_tonespace())
