#!/usr/bin/env python3

import numpy as np
from tone import Tone

'''
Takes in a tone and splits it up into equal parts of a desired period or fraction.
'''
class ToneSplitter:

    '''
    This class takes in a tone and performs operations on it, returning the data for the signal.

    Example use:

    tone = Tone(1000) # your usual 1000 hertz tone
    splitter = ToneSplitter(tone)
    splitter.subdivide(3) #split the 1000 hertz tone into 3 parts

    part1 = splitter.Next()
    part2 = splitter.Next()
    part3 = splitter.Next()

    splitter.rewind()
    splitter.setperiod(1/2500)
    segment1 = splitter.Next()
    segment2 = splitter.Next()
    '''
    def __init__(self, tone: Tone): #samplerate = samples in a second
        self.samplerate = tone.get_samplerate()
        self.frequency = tone.get_frequency()
        self.period = 1/self.frequency
        self.tone = tone
        self.tonedata = tone.evaluate()
        self.subdivide(1)
        self.index=0

    '''
    split the tone up into k equal bits
    '''
    def subdivide(self,k):
        self.period = 1/(self.frequency*k)

    '''
    split the tone up so that each equal segment has a specified period
    '''
    def setperiod(self,period):
        self.period = period
        #probably doesn't have to be divisible
        # self.period = period - period % (1/samplerate)

    '''
    return the raw data for the next segment of the whole tone.
    '''
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
    reset the index of the segments back to the first one
    '''
    def rewind(self):
        self.index=0

    def get_tone(self):
        return self.tone

    def get_period(self):
        return self.period

    def get_frequency(self):
        return self.frequency
