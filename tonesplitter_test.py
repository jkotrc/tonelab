from tonesplitter import ToneSplitter
from tone import Tone
import pytest
import numpy as np
'''
Testing whether:
- next without subdivision gives the right tone
- halving a tone works by comparing two nexts to the original signal
- setting a period works by comparing a single next to a truncated version of the original signal
'''

frequency=10
samplerate=44100

class TestToneSplitter:
    @pytest.fixture
    def splitter(self):
        _tone = Tone(frequency)
        return ToneSplitter(_tone)

    def testsplitternotnull(self, splitter):
        assert len(splitter.get_tone().evaluate()) > 0

    def test_subdivision_by_3(self, splitter):
        splitter.subdivide(3)
        assert splitter.get_period() == (1/3)*(1/splitter.get_frequency())

    def test_nominal(self, splitter):
        tone1 = splitter.get_tone().evaluate()
        tone2 = splitter.Next()
        assert (tone1 == tone2).all()

    def test_half_size(self, splitter):
        splitter.subdivide(2)
        tone1 = splitter.get_tone().evaluate()
        tone2 = splitter.Next()
        assert len(tone1) == 2*len(tone2)
        tone3 = splitter.Next()
        assert len(tone2) == len(tone3)

    def test_half(self, splitter):
        splitter.subdivide(2)
        tone1 = splitter.get_tone().evaluate()
        tone2 = splitter.Next()
        tone2 = np.append(tone2,splitter.Next())
        assert len(tone1) == len(tone2)
        assert (tone1 == tone2).all()

    def test_period(self, splitter):
        period = (1/9) - (1/9) % (1/samplerate)
        tone1 = splitter.get_tone().evaluate()[0:int(period*samplerate)]
        tone2 = splitter.Next()
        assert (tone1 == tone2).all()

    def test_period_several(self, splitter):
        # period = (1/12) - (1/12) % (1/samplerate)
        period = 1/12
        tone1 = splitter.Next()
        space = np.linspace(0, 1/frequency, int(samplerate/frequency))
        arr = space
        for i in range(0,12):
            tone1 = np.append(tone1, splitter.Next())
            arr = np.append(arr,space)
        arr = np.sin(2*np.pi*arr*frequency)
        assert len(tone1) == len(arr)
        np.testing.assert_array_almost_equal(tone1,arr)
