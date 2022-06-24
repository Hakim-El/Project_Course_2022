import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import pyroomacoustics as pra
from sklearn.metrics import mean_squared_error
import os
import _modules.SineSweep_stimulus as stim
from _modules.Calibration import calibrate

### IMPORTANT: This script is not used in the RIR Framework but it is implemented in the 
### Calibration_OLD module from Project Course 2021 exam and it can be used to perform some 
## simulations with pyroomacoustics

# Room dimensions
xlim=3.64
ylim=5
zlim=3

# Sampling frequency
fs=96000

# SNR in dB
SNRdb = 5

# We invert Sabine's formula to obtain the parameters for the ISM simulator
mat = pra.make_materials(
    ceiling="fibre_absorber_1",
    floor="carpet_tufted_9.5mm",
    east="fibre_absorber_1",
    west="fibre_absorber_1",
    north="fibre_absorber_1",
    south="fibre_absorber_1"
)

max_order = 17

#fig, ax = room.plot()
#ax.set_xlim([-1, 6])
#ax.set_ylim([-1, 4])

# specify signal source
testStimulus = stim.stimulus('sinesweep',fs)
testStimulus.generate(fs, 10, 0.2,1,1, 1, [0 , 0])
signal = testStimulus.signal.reshape(testStimulus.signal.shape[0],)

micLocs = np.c_[
        [0.6, 4.4, 0.7],
        [1.2, 4.4, 0.7],
        [1.8, 4.4, 0.7],
        [2.4, 4.4, 0.7],
        [3,   4.4, 0.7],
        [0.6, 4.4, 1.4],
        [1.2, 4.4, 1.4],
        [1.8, 4.4, 1.4],
        [2.4, 4.4, 1.4],
        [3,   4.4, 1.4],
        [0.6, 4.4, 2.1],
        [1.2, 4.4, 2.1],
        [1.8, 4.4, 2.1],
        [2.4, 4.4, 2.1],
        [3,   4.4, 2.1],

        [0.6, 3.8, 0.7],
        [1.2, 3.8, 0.7],
        [1.8, 3.8, 0.7],
        [2.4, 3.8, 0.7],
        [3,   3.8, 0.7],
        [0.6, 3.8, 1.4],
        [1.2, 3.8, 1.4],
        [1.8, 3.8, 1.4],
        [2.4, 3.8, 1.4],
        [3,   3.8, 1.4],
        [0.6, 3.8, 2.1],
        [1.2, 3.8, 2.1],
        [1.8, 3.8, 2.1],
        [2.4, 3.8, 2.1],
        [3,   3.8, 2.1],

        [0.6, 3.2, 0.7],
        [1.2, 3.2, 0.7],
        [1.8, 3.2, 0.7],
        [2.4, 3.2, 0.7],
        [3,   3.2, 0.7],
        [0.6, 3.2, 1.4],
        [1.2, 3.2, 1.4],
        [1.8, 3.2, 1.4],
        [2.4, 3.2, 1.4],
        [3,   3.2, 1.4],
        [0.6, 3.2, 2.1],
        [1.2, 3.2, 2.1],
        [1.8, 3.2, 2.1],
        [2.4, 3.2, 2.1],
        [3,   3.2, 2.1],

        [0.6, 2.6, 0.7],
        [1.2, 2.6, 0.7],
        [1.8, 2.6, 0.7],
        [2.4, 2.6, 0.7],
        [3,   2.6, 0.7],
        [0.6, 2.6, 1.4],
        [1.2, 2.6, 1.4],
        [1.8, 2.6, 1.4],
        [2.4, 2.6, 1.4],
        [3,   2.6, 1.4],
        [0.6, 2.6, 2.1],
        [1.2, 2.6, 2.1],
        [1.8, 2.6, 2.1],
        [2.4, 2.6, 2.1],
        [3,   2.6, 2.1],

        [0.6, 2, 0.7],
        [1.2, 2, 0.7],
        [1.8, 2, 0.7],
        [2.4, 2, 0.7],
        [3,   2, 0.7],
        [0.6, 2, 1.4],
        [1.2, 2, 1.4],
        [1.8, 2, 1.4],
        [2.4, 2, 1.4],
        [3,   2, 1.4],
        [0.6, 2, 2.1],
        [1.2, 2, 2.1],
        [1.8, 2, 2.1],
        [2.4, 2, 2.1],
        [3,   2, 2.1],

        [0.6, 1.4, 0.7],
        [1.2, 1.4, 0.7],
        [1.8, 1.4, 0.7],
        [2.4, 1.4, 0.7],
        [3,   1.4, 0.7],
        [0.6, 1.4, 1.4],
        [1.2, 1.4, 1.4],
        [1.8, 1.4, 1.4],
        [2.4, 1.4, 1.4],
        [3,   1.4, 1.4],
        [0.6, 1.4, 2.1],
        [1.2, 1.4, 2.1],
        [1.8, 1.4, 2.1],
        [2.4, 1.4, 2.1],
        [3,   1.4, 2.1],

        [0.6, 0.8, 0.7],
        [1.2, 0.8, 0.7],
        [1.8, 0.8, 0.7],
        [2.4, 0.8, 0.7],
        [3,   0.8, 0.7],
        [0.6, 0.8, 1.4],
        [1.2, 0.8, 1.4],
        [1.8, 0.8, 1.4],
        [2.4, 0.8, 1.4],
        [3,   0.8, 1.4],
        [0.6, 0.8, 2.1],
        [1.2, 0.8, 2.1],
        [1.8, 0.8, 2.1],
        [2.4, 0.8, 2.1],
        [3,   0.8, 2.1],         
        ]

knownPos = np.array([[1.55, 0, 1.67],
                           [1.625, 0, 1.445],
                           [1.7, 0, 1.67],
                           [1.775, 0, 1.445],
                           [1.85, 0, 1.67],
                           [1.925, 0, 1.445],
                           [2, 0, 1.67],
                           [2.075, 0, 1.52]])

def computeRIR1(SNRdb=0):

    room = pra.ShoeBox([xlim, ylim, zlim], fs=fs, materials=mat, max_order=17, air_absorption=True, ray_tracing=False)

    outputChannels = knownPos.shape[0]

    # adding sources to the room
    for i in range(0,outputChannels):
        room.add_source(knownPos[i,:], signal=signal, delay=0)

    # add mics
    room.add_microphone_array(micLocs)

    micSigs = room.simulate(return_premix=True)
    micSigs = micSigs[:,:,0:signal.shape[0]]

    if SNRdb != 0:
        noise = np.random.normal(0,1,micSigs.shape[2])
        for l in range(micSigs.shape[0]):
            for m in range(micSigs.shape[1]):
                SNR = 10**(SNRdb/10)
                Ps = np.sum(np.abs(micSigs[l,m,:])**2)/micSigs.shape[2] # Signal Power
                Pn = np.sum(np.abs(noise)**2)/len(noise)                # noise Power
                alpha = np.sqrt(Ps/(SNR*Pn))
                micSigs[l,m,:] = micSigs[l,m,:] + alpha*noise
    
    RIRlength = (len(testStimulus.invfilter)+micSigs.shape[2]-1)//2 +1
    nMics = micSigs.shape[1]
    nLS = micSigs.shape[0]

    data = np.zeros((RIRlength,nMics,nLS))

    for l in np.arange(0,nLS):
        for m in np.arange(0,nMics):
            RIR = fftconvolve(testStimulus.invfilter,micSigs[l,m,:])
            RIRtoSave = RIR[RIR.shape[0]//2:]
            data[:,m,l] = RIRtoSave

    dirname = 'SineSweepMeasures/SimtestNoise5dB'
    np.save(dirname + '/RIRMatrix.npy',data)

    return data

directory = 'SineSweepMeasures/SimtestNoise5dB/RIRMatrix.npy'
if os.path.isfile(directory):
    data1 = np.load(directory)
else:
    data1 = computeRIR1(SNRdb)

# CALIBRATION
posbounds = [[0,3.3],[0,5],[0,2.8]]
measureName = 'SimtestNoise5dB'

estimatedPosition, estimatedBuffer=calibrate(data1,fs,measureName,1,position_type='s',positions=knownPos,max_buffer=1e-3,positions_bounds=posbounds, interp_factor=2,estimate_buffer=False)

# MSE
truePosMic = np.transpose(micLocs, (1, 0))
micCalibrationError = mean_squared_error(truePosMic,estimatedPosition)
print('MSE1 : ' + str(micCalibrationError))


####################################################################################
####################################################################################

LsPositions = np.array([
    [1.4, 3.4, 1.2],
    [2.2, 3.4, 1.2],
    [1.4, 2.6, 1.2],
    [2.2, 2.6, 1.2],
    [1.4, 1.8, 1.2],
    [2.2, 1.8, 1.2],
])

def computeRIR2(SNRdb=0):

    # create the room for the secon measurement

    room2 = pra.ShoeBox([xlim, ylim, zlim], fs=fs, materials=mat, max_order=17, air_absorption=True, ray_tracing=False)

    outputChannels = LsPositions.shape[0]

    # adding sources to the room
    for i in range(0,outputChannels):
        room2.add_source(LsPositions[i,:], signal=signal, delay=0)

    room2.add_microphone_array(micLocs)

    micSigs2 = room2.simulate(return_premix=True)
    micSigs2 = micSigs2[:,:,0:signal.shape[0]]

    if SNRdb != 0:
        noise = np.random.normal(0,1,micSigs2.shape[2])
        for l in range(micSigs2.shape[0]):
            for m in range(micSigs2.shape[1]):
                SNR = 10**(SNRdb/10)
                Ps = np.sum(np.abs(micSigs2[l,m,:])**2)/micSigs2.shape[2] # Signal Power
                Pn = np.sum(np.abs(noise)**2)/len(noise)                # noise Power
                alpha = np.sqrt(Ps/(SNR*Pn))
                micSigs2[l,m,:] = micSigs2[l,m,:] + alpha*noise

    RIRlength = (len(testStimulus.invfilter)+micSigs2.shape[2]-1)//2 +1
    nMics = micSigs2.shape[1]
    nLS = micSigs2.shape[0]

    data = np.zeros((RIRlength,nMics,nLS))

    for l in np.arange(0,nLS):
        for m in np.arange(0,nMics):
            RIR = fftconvolve(testStimulus.invfilter,micSigs2[l,m,:])
            RIRtoSave = RIR[RIR.shape[0]//2:]
            data[:,m,l] = RIRtoSave

    dirname = 'SineSweepMeasures/SimtestNoise5dB2'
    np.save(dirname + '/RIRMatrix.npy',data)

    return data

directory = 'SineSweepMeasures/SimtestNoise5dB2/RIRMatrix.npy'
if os.path.isfile(directory):
    data2 = np.load(directory)
else:
    data2 = computeRIR2(SNRdb)

# CALIBRATION
measureName = 'SimtestNoise5dB2'
knownPos = estimatedPosition
posbounds2 = [[0,2.6],[0,4],[0,1.5]]

estimatedPosition2, estimatedBuffer=calibrate(data2,fs,measureName,1,position_type='m',positions=knownPos,max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)

# MSE
micCalibrationError2 = mean_squared_error(LsPositions,estimatedPosition2)
print('MSE2 : ' + str(micCalibrationError2))