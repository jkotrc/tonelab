#!/usr/bin/env python3

import numpy as np
from tone import Tone

'''
A class representing a single period of a tone with some frequency. It allows
you to divide the tone into segments so that they can be played quickly in succession,
even if the period of the signal is too large to play for the specified frequency.

Also stores a samplerate variable for determining the samplerate of the sound file
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
    def __init__(self, tone: Tone): #samplerate = samples in a second
        self.samplerate = tone.get_samplerate()
        self.frequency = tone.get_frequency()
        self.period = 1/self.frequency
        self.tone = tone
        self.tonedata = tone.evaluate()
        self.subdivide(1)
        self.index=0

    #TODO this has a new meaning now
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
        self.period = period - period % (1/samplerate)

    # TODO make this class an iterator?
    def Next(self):
        segment=[]
        N = int(self.samplerate/self.frequency)
        start = int((self.period*self.samplerate*self.index) % N)
        offset = start + int((self.period*self.samplerate))
        while offset > len(self.tonedata):
            segment.extend(self.tonedata[start:len(self.tonedata)])
            offset -= len(self.tonedata) - start
            start=0
        if offset != 0:
            segment.extend(self.tonedata[start:offset])
        self.index+=1
        return np.array(segment)

    '''
    Reset the index of the sequence of fractions back to 0.
    '''
    def rewind(self):
        self.index=0
