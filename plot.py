#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from tone import Tone

frequency = 10
segments = 12
bitrate = 44100
padding = 1
t = Tone(frequency,bitrate)
t.subdivide(segments)
x = np.linspace(0, 3/frequency, int(bitrate/frequency)+segments*padding)

y = t.Next()
for i in range(0,segments-1):
    y=np.append(y, np.zeros(padding))
    y=np.append(y, t.Next())
y = np.append(y,np.zeros(len(x)-len(y)))
plt.plot(x,y)
plt.show()
