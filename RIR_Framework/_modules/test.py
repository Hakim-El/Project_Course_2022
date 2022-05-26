import numpy as np
from Calibration3 import calibrate
from Calibration3 import find_directPath
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

RIR = np.load('RIRMatrix.npy')
RIR = np.moveaxis(RIR,(0,1,2),(1,2,0))
plt.plot(RIR[:,12,3])
plt.show()
c = 331.3 + 0.606*20
direct = find_directPath(RIR[38715:,0,0])
print(direct/96000*c)
fs = 96000
#pos = np.array([[1.55,0,1.67],[1.55,0,1.58],[1.61,0,1.67],[1.64,0,1.58],[1.67,0,1.58],[1.7,0,1.67],[1.73,0,1.58],[1.76,0,1.67]])
pos = np.array([[0,0,0],[7.5,0,-7.5*3],[7.5*2,0,0],[7.5*3,0,-7.5*3],[7.5*4,0,0],[7.5*5,0,-7.5*3],[7.5*6,0,0],[7.5*7,0,-7.5*3]])/100
pos_shift = np.array([1.55,0,1.67])
pos = pos + pos_shift
#pos = np.transpose(pos)
positiontype = 's'
max_buffer = 1e-3
interp_factor = 2
posbounds = [[0,3.64],[0,5],[0,2.5]]

RIR = RIR[12690:12690+fs,:,:]
pos_est, buffer_est = calibrate(RIR,fs,positiontype,pos,max_buffer,posbounds,interp_factor,sound_speed=c, estimate_buffer=False)
print(pos_est)
print(buffer_est)
print(cdist(pos_est,pos_est))