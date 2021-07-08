import numpy as np
import pytest
import tone

frequency = 20
class TestTone:
    @pytest.fixture
    def _tone(self):
        a = tone.Tone(frequency)
        return a

    def test_spacenotnull(self, _tone):
        assert len(_tone.get_tonespace()) > 0

    def test_spacecorrect(self, _tone):
        space1 = _tone.get_tonespace()
        space2 = np.linspace(0, 1/frequency, int(np.ceil(44100/frequency)))
        assert (space1 == space2).all()

    def test_valuescorrect(self, _tone):
        vals1 = _tone.evaluate()
        vals2 = np.sin(np.linspace(0, 1/frequency, int(np.ceil(44100/frequency))))
        assert (vals1 == vals2).all()
