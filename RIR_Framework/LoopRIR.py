import numpy as np
import matplotlib.pyplot as plt
from _modules.Calibration3 import find_peaks
from _modules.Calibration3 import find_directPath

RIR = np.load('SineSweepMeasures/loop3/RIR.npy')
RIR = RIR.reshape((RIR.shape[0],))
plt.plot(RIR[12000:12000+10000])
plt.show()

peak = find_directPath(RIR)
print(peak)

print(RIR.shape)