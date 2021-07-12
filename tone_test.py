import numpy as np
import pytest
import tone

frequency = 20
samplerate = 44100

def sinepluscosine(x: float, freq: float):
    arg = 2*np.pi*freq
    return np.sin(arg*x)+np.cos(arg*x)

class TestTone:
    @pytest.fixture
    def _tone(self):
        a = tone.Tone(frequency)
        return a

    def test_spacenotnull(self, _tone):
        assert len(tone.Tone.get_tonespace(1/frequency,samplerate)) > 0

    def test_spacecorrect(self, _tone):
        space1 = tone.Tone.get_tonespace(1/frequency,samplerate)
        space2 = np.linspace(0, 1/frequency, int(np.ceil(samplerate/frequency)))
        assert (space1 == space2).all()

    def test_values(self, _tone):
        tonespace1=tone.Tone.get_tonespace(1/frequency,samplerate)
        tonespace2=np.linspace(0, 1/frequency, int(np.ceil(samplerate/frequency)))
        assert (tonespace1 == tonespace2).all()
        vals1 = _tone.evaluate()
        vals2 = np.sin(2*np.pi*frequency*tonespace2)
        assert (vals1 == vals2).all()

    def test_values_different_generator(self):
        _tone = tone.Tone(frequency, lambda x: sinepluscosine(x, frequency))
        tonespace1=tone.Tone.get_tonespace(1/frequency,samplerate)
        tonespace2=np.linspace(0, 1/frequency, int(np.ceil(samplerate/frequency)))
        assert (tonespace1 == tonespace2).all()
        vals1 = _tone.evaluate()
        vals2 = np.sin(2*np.pi*frequency*tonespace2) + np.cos(2*np.pi*frequency*tonespace2)
        np.testing.assert_array_almost_equal(vals1,vals2)
        # assert (vals1 == vals2).all()
