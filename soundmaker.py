from scipy.io.wavfile import write
import numpy as np

from tone import Tone
from tonesplitter import ToneSplitter

samplerate=44100

#TODO type hints for float ndarray
def make_sound(data, scalefactor):
    if data.dtype != 'float64':
        raise ValueError(f"{type(data)} not a float array!")
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write('test.wav', samplerate,scaled)

'''
1000hz, 1000 times per second with 10*10^-4 = 1/1000 s breaks
'''
def thousandthousand():
    t = Tone(1000, samplerate=samplerate)
    splitter = ToneSplitter(t)
    splitter.setperiod()
