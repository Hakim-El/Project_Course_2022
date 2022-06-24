import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import pyroomacoustics as pra
import _modules.SineSweep_stimulus as stim
from _modules.Calibration import calibrate
from sklearn.metrics import mean_squared_error
import os

# Room dimensions
xlim=3.64
ylim=5
zlim=3

# Sampling frequency
fs=96000

mat = pra.make_materials(
    ceiling="fibre_absorber_1",
    floor="carpet_tufted_9.5mm",
    east="fibre_absorber_1",
    west="fibre_absorber_1",
    north="fibre_absorber_1",
    south="fibre_absorber_1"
)

max_order = 17

# specify signal source
testStimulus = stim.stimulus('sinesweep',fs)
testStimulus.generate(fs, 10, 0.2,1,1, 1, [0 , 0])
signal = testStimulus.signal.reshape(testStimulus.signal.shape[0],)

room = pra.ShoeBox([xlim, ylim, zlim], fs=fs, materials=mat, max_order=17, air_absorption=True, ray_tracing=False)

room.add_source(np.array([1.55,0,1.67]), signal=signal, delay=0)

room.add_microphone(np.array([1.2, 3.8, 1.4]))

room.compute_rir()
impulseRIR = room.rir[0][0]

micSigs = room.simulate(return_premix=True)
micSigs = micSigs[:,:,0:signal.shape[0]]

RIRlength = (len(testStimulus.invfilter)+micSigs.shape[2]-1)//2 +1
nMics = micSigs.shape[1]
nLS = micSigs.shape[0]

data = np.zeros((RIRlength,nMics,nLS))
for l in np.arange(0,nLS):
    for m in np.arange(0,nMics):
        RIR = fftconvolve(testStimulus.invfilter,micSigs[l,m,:])
        RIRtoSave = RIR[RIR.shape[0]//2:]
        data[:,m,l] = RIRtoSave

data = data[:len(impulseRIR),0,0]

error = mean_squared_error(impulseRIR,data)

print('The mean square error between a sinesweep and an impulse RIR is: ' + str(error))