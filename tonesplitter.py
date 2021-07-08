#!/usr/bin/env python3

import numpy as np

'''
A class representing a single period of a tone with some frequency. It allows
you to divide the tone into segments so that they can be played quickly in succession,
even if the period of the signal is too large to play for the specified frequency.

Also stores a bitrate variable for determining the bitrate of the sound file
'''

'''
This shouldn't be a "Tone" class because it just represents one of the possible mechanisms.
The other thing that one could do is overlaying the tones over each other with a certain separation
to see what that does, possibly with some additional features.

- There should be a pretty primitive Tone class with WAV integration, some utilities and abstractions
from a simple array of values.

- All operations should use this class (graphing, splitting the tone, etc.)

- ToneFactory?

- ToneSplitter class for this functionality, ToneStacker for superimposition?

- General sound configuration?

- Graphical user interface?
"
'''
class ToneSplitter:
    def __init__(self, frequency, bitrate: int=44100): #bitrate = samples in a second
        self.bitrate = bitrate
        # 1/f must be divisible by 1/b
        self.period = 1/frequency
        self.period -= self.period % (1/bitrate)
        self.frequency = 1/self.period
        # Make an x axis going from 0 to the period of the tone.
        self.tone = np.linspace(0, 1/self.frequency, int(self.bitrate/self.frequency))
        # Make it a wave by taking the sine of each number in the array
        # TODO convert to integers
        self.tone = np.sin(2*np.pi*self.tone*self.frequency)
        self.subdivide(1)
        self.index=0

    def get_tone(self):
        return self.tone

    def get_period(self):
        return self.period

    def get_frequency(self):
        return self.frequency
    '''
    Divide the tone by a factor of k. k=1 gives the whole wave, k=0.5 splits it into two.
    This makes tones with a period of T=1/kf. The whole wave is just T=1/f as expected.

    If the tone cannot be divided into k equally spaced pieces, repeat the tone and add to the
    incomplete piece from the start. This may cause a very long (possibly infinite)
    sequence of unique tones.
    '''
    def subdivide(self,k):
        self.period = 1/(self.frequency*k)

    '''
    Set the divisor to make tones of some period T. This function looks for the right divisor
    k by rearranging the equation: T=1/kf leads to k = 1/Tf, where we choose the period, know the frequency
    and set k.
    '''
    def setperiod(self,period):
        self.period = period - period % (1/bitrate)

    # TODO make this class an iterator?
    def Next(self):
        segment=[]
        N = int(self.bitrate/self.frequency)
        start = int((self.period*self.bitrate*self.index) % N)
        offset = start + int((self.period*self.bitrate))
        while offset > len(self.tone):
            segment.extend(self.tone[start:len(self.tone)])
            offset -= len(self.tone) - start
            start=0
        if offset != 0:
            segment.extend(self.tone[start:offset])
        self.index+=1
        return np.array(segment)

    '''
    Reset the index of the sequence of fractions back to 0.
    '''
    def rewind(self):
        self.index=0
