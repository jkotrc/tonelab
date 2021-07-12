import numpy as np
from typing import Protocol
import math

'''
helper class used to make sure that user-defined signal functions have the right type and to
set the default function to a sine wave
'''
class ToneGenerator(Protocol):
    @staticmethod
    def sine_wave(frequency):
        return lambda x: np.sin(2*np.pi*frequency*x)

    def __call__(self, x: float) -> float:
        return self(x)

'''
Represents one period of some periodic function. This is the sort of basic object of the program
that will be taken in by various utilities to make different sounds.
'''
class Tone:
    '''
    Utility method to get the correct (discrete) X-axis (or rather T-axis) for whatever tone.
    This would be an axis from 0 to the duration of the tone, with a step size of 1/samplerate
    '''
    @staticmethod
    def get_tonespace(length, samplerate):
        return np.linspace(0,length,int(np.ceil(samplerate * length)))
        # return np.linspace(0,1/frequency, int(np.ceil(samplerate/frequency)))

    '''
    The constructor.
    Arguments:
    frequency: the frequency of the tone
    (optional) generator: the function to use to make the tone. If unspecified, a sine wave will be used.
                          Note that this function has to be periodic over the period of the signal (T=1/f).
                          so f(0) must equal f(1/f)
    (optional) samplerate: set a custom samplerate. Set to 44100 by default

    Examples:
    tone = Tone(1000) # make a 1000 Hertz sine wave with 44100 samples per second
    tone = Tone(2000, samplerate=10000) # 2000Hz sine wave with 10000 samples per second

    # example function you could define instead of the default sine wave
    def sinpluscos(x, freq):
        arg = 2*np.pi*freq #2*pi*freq makes the sine and cosine periodic over 0,1/f
        return sin(arg*x)+cos(arg*x)

    tone = Tone(1000, lambda x: sinpluscos(x,1000)) # make a tone using sin(2pi f x)+cos(2pi f x)
    '''
    def __init__(self, frequency, generator: ToneGenerator=None, samplerate=44100): #samplerate = samples per second
        self.samplerate=samplerate
        self.frequency=frequency
        if generator is None:
            generator=ToneGenerator.sine_wave(self.frequency)
        self.generator=generator
        if not math.isclose(generator(0),generator(1/self.frequency), rel_tol=1e-06, abs_tol=1e-06):
            raise ValueError(f"Function not periodic over [{0},{1/self.frequency}]!\n expected {generator(0)} == {generator(1/self.frequency)}")

    def __eq__(self, other):
        samefreq = (self.frequency == other.frequency)
        samevals = (self.evaluate() == other.evaluate()).all()
        return (samefreq and samevals)

    '''
    return the tone as a raw data array
    '''
    def evaluate(self):
        return self.generator(Tone.get_tonespace(1/self.frequency, self.samplerate))

    def get_frequency(self):
        return self.frequency

    def get_samplerate(self):
        return self.samplerate
