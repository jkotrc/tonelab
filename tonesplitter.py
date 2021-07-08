#!/usr/bin/env python3

import numpy as np
from tone import Tone

class ToneSplitter:
    def __init__(self, tone: Tone): #samplerate = samples in a second
        self.samplerate = tone.get_samplerate()
        self.frequency = tone.get_frequency()
        self.period = 1/self.frequency
        self.tone = tone
        self.tonedata = tone.evaluate()
        self.subdivide(1)
        self.index=0

    def subdivide(self,k):
        self.period = 1/(self.frequency*k)

    def setperiod(self,period):
        self.period = period
        #probably doesn't have to be divisible
        # self.period = period - period % (1/samplerate)

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

    def rewind(self):
        self.index=0

    def get_tone(self):
        return self.tone

    def get_period(self):
        return self.period

    def get_frequency(self):
        return self.frequency
