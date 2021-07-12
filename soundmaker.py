from scipy.io.wavfile import write
import numpy as np

from tone import Tone
from tonesplitter import ToneSplitter

samplerate=44100

#TODO type hints for float ndarray
def make_sound(data, scalefactor=32767):
    if data.dtype != 'float64':
        raise ValueError(f"{type(data)} not a float array!")
    scaled = np.int16(data/np.max(np.abs(data)) * scalefactor)
    write('test.wav', samplerate,scaled) #TODO check if filename exists

'''
1000hz, 1000 times per second.
Let T denote the period of each signal segment and B the length of the break.
Then 1000*(T+B)=1, T+B = 1/1000, where T,B < 1/1000 since they both have to be positive.

choose 1/1100 long breaks.
T+1/1100=1/1000
1/1000-1/1100 = T
'''

#breaks of length 1/1100
#normal sine wave
def thousandthousand(duration): #duration in seconds
    break_length = 1/1100
    period = 1/1000-break_length
    t = Tone(1000, samplerate=samplerate)
    splitter = ToneSplitter(t)
    splitter.setperiod(period)
    silence = np.zeros(int(np.ceil(break_length*samplerate)))
    sound = splitter.Next()
    sound = np.append(sound,silence)
    for i in range(0, duration*1000-1):
        sound = np.append(sound,splitter.Next())
        sound = np.append(sound,silence)
    make_sound(sound)

if __name__ == "__main__":
    thousandthousand(3)
