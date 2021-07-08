import tone
import pytest
import numpy as np
'''
Testing whether:
- next without subdivision gives the right tone
- halving a tone works by comparing two nexts to the original signal
- setting a period works by comparing a single next to a truncated version of the original signal
'''

frequency=10
bitrate=44100

#TODO nothing runs!
class TestTone:
    @pytest.fixture
    def _tone(self):
        return tone.Tone(frequency)

    def test_tonenotnull(self, _tone):
        assert len(_tone.get_tone()) > 0

    def test_subdivision_by_3(self, _tone):
        _tone.subdivide(3)
        assert _tone.get_period() == (1/3)*(1/_tone.get_frequency())

    def test_types(self, _tone):
        arr = _tone.get_tone()
        arr2 = _tone.Next()
        assert type(arr) == type(np.ones(len(arr)))
        assert type(arr2) == type(np.ones(len(arr2)))

    def test_nominal(self, _tone):
        tone1 = _tone.get_tone()
        tone2 = _tone.Next()
        assert (tone1 == tone2).all()

    def test_half_size(self, _tone):
        _tone.subdivide(2)
        tone1 = _tone.get_tone()
        tone2 = _tone.Next()
        assert len(tone1) == 2*len(tone2)
        tone3 = _tone.Next()
        assert len(tone2) == len(tone3)

    def test_half(self, _tone):
        _tone.subdivide(2)
        tone1 = _tone.get_tone()
        tone2 = _tone.Next()
        tone2 = np.append(tone2,_tone.Next())
        assert len(tone1) == len(tone2)
        assert (tone1 == tone2).all()

    def test_period(self, _tone):
        period = (1/9) - (1/9) % (1/bitrate)
        tone1 = _tone.get_tone()[0:int(period*bitrate)]
        tone2 = _tone.Next()
        assert (tone1 == tone2).all()

    def test_period_several(self, _tone):
        period = (1/12) - (1/12) % (1/bitrate)
        tone1 = _tone.Next()
        space = np.linspace(0, 1/frequency, int(bitrate/frequency))
        arr = space
        for i in range(0,12):
            tone1 = np.append(tone1, _tone.Next())
            arr = np.append(arr,space)
        arr = np.sin(2*np.pi*arr*frequency)
        assert len(tone1) == len(arr)
        assert (tone1 == arr).all()
