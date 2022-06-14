import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import pyroomacoustics as pra
import _modules.SineSweep_stimulus as stim
from _modules.Calibration import calibrate
from sklearn.metrics import mean_squared_error
import os

### IMPORTANT: This script is not used in the RIR Framework but it is implemented in the 
### Calibration_OLD module from Project Course 2021 exam and it can be used to perform some 
## simulations with pyroomacoustics

# Creates a simulation of a RIR with 4 Loudspeakers and 1 mic at determined positions
# Used for testing the calibration algorithm
# Predetermined room shape for testing: x = 5m , y = 5m for the 2D case, z = 3m for 3D

# Room dimensions
xlim=3.64
ylim=5
zlim=3

# Sampling frequency
fs=44100

# The desired reverberation time and dimensions of the room
rt60 = 0.1  # seconds

# We invert Sabine's formula to obtain the parameters for the ISM simulator
e_absorption, _ = pra.inverse_sabine(rt60, [xlim,ylim,zlim])
max_order = 10
corners = np.array([[0,0], [0,ylim], [xlim,ylim], [xlim,0]]).T  # [x,y]

#fig, ax = room.plot()
#ax.set_xlim([-1, 6])
#ax.set_ylim([-1, 4])

# specify signal source
testStimulus = stim.stimulus('sinesweep',fs)
testStimulus.generate(fs, 10, 0.2,1,1, 1, [0 , 0])
signal = testStimulus.signal.reshape(testStimulus.signal.shape[0],)
#signal = pra.experimental.signals.exponential_sweep(10, fs, f_lo=0.0, f_hi=None, fade=None, ascending=False)
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

def computeRIR1():

    # set max_order to a low value for a quick (but less accurate) RIR
    room = pra.Room.from_corners(corners, fs=fs, max_order=max_order, materials=pra.Material(e_absorption), ray_tracing=False, air_absorption=True)
    room.extrude(zlim)

    # Set the ray tracing parameters
    #room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)

    outputChannels = knownPos.shape[0]

    # adding sources to the room
    for i in range(0,outputChannels):
        room.add_source(knownPos[i,:], signal=signal, delay=0)

    # add mics
    room.add_microphone_array(micLocs)

    # compute image sources
    room.image_source_model()

    # visualize 3D polyhedron room and image sources
    #fig, ax = room.plot(img_order=3)
    #fig.set_size_inches(18.5, 10.5)

    # compute RIR
    room.compute_rir()
    #data = np.zeros((RIRlen,outputChannels))
    #for i in np.arange(0,4):
    #    data[:RIRlen,i] = room.rir[0][i][:RIRlen]

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

    dirname = 'SineSweepMeasures/Simtest'
    np.save(dirname + '/RIRMatrix.npy',data)

    return data

directory = 'SineSweepMeasures/Simtest/RIRMatrix.npy'
if os.path.isfile(directory):
    data = np.load(directory)
else:
    data = computeRIR1()

# CALIBRATION
posbounds = [[0,3.3],[0,5],[0,2.8]]
measureName = 'Simtest'

estimatedPosition, estimatedBuffer=calibrate(data,fs,measureName,1,position_type='s',positions=knownPos,max_buffer=1e-3,positions_bounds=posbounds, interp_factor=2,estimate_buffer=False)

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

def computeRIR2():

    # create the room for the secon measurement
    room2 = pra.Room.from_corners(corners, fs=fs, max_order=max_order, materials=pra.Material(e_absorption), ray_tracing=False, air_absorption=True)
    room2.extrude(zlim)

    outputChannels = LsPositions.shape[0]

    # adding sources to the room
    for i in range(0,outputChannels):
        room2.add_source(LsPositions[i,:], signal=signal, delay=0)

    room2.add_microphone_array(micLocs)

    room2.image_source_model()
    room2.compute_rir()

    micSigs2 = room2.simulate(return_premix=True)
    micSigs2 = micSigs2[:,:,0:signal.shape[0]]
    RIRlength = (len(testStimulus.invfilter)+micSigs2.shape[2]-1)//2 +1
    nMics = micSigs2.shape[1]
    nLS = micSigs2.shape[0]

    data = np.zeros((RIRlength,nMics,nLS))

    for l in np.arange(0,nLS):
        for m in np.arange(0,nMics):
            RIR = fftconvolve(testStimulus.invfilter,micSigs2[l,m,:])
            RIRtoSave = RIR[RIR.shape[0]//2:]
            data[:,m,l] = RIRtoSave

    dirname = 'SineSweepMeasures/Simtest2'
    np.save(dirname + '/RIRMatrix.npy',data)

    return data

directory = 'SineSweepMeasures/Simtest2/RIRMatrix.npy'
if os.path.isfile(directory):
    data = np.load(directory)
else:
    data = computeRIR2()

# CALIBRATION
measureName = 'Simtest2'
knownPos = estimatedPosition
posbounds2 = [[0,2.6],[0,4],[0,1.5]]

#estimatedPosition2, estimatedBuffer=calibrate(data,fs,measureName,1,position_type='m',positions=knownPos,max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)

# MULTIPLE CALIBRATION TEST

estimatedPos1 , estimatedBuffer =calibrate(data[:,0:15,:],fs,measureName,1,position_type='m',positions=knownPos[0:15,:],max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)
estimatedPos2 , estimatedBuffer =calibrate(data[:,15:30,:],fs,measureName,1,position_type='m',positions=knownPos[15:30,:],max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)
estimatedPos3 , estimatedBuffer =calibrate(data[:,30:45,:],fs,measureName,1,position_type='m',positions=knownPos[30:45,:],max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)
estimatedPos4 , estimatedBuffer =calibrate(data[:,45:60,:],fs,measureName,1,position_type='m',positions=knownPos[45:60,:],max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)
estimatedPos5 , estimatedBuffer =calibrate(data[:,60:75,:],fs,measureName,1,position_type='m',positions=knownPos[60:75,:],max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)
estimatedPos6 , estimatedBuffer =calibrate(data[:,75:90,:],fs,measureName,1,position_type='m',positions=knownPos[75:90,:],max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)
estimatedPos7 , estimatedBuffer =calibrate(data[:,90:,:],fs,measureName,1,position_type='m',positions=knownPos[90:,:],max_buffer=1e-3,positions_bounds=posbounds2, interp_factor=2,estimate_buffer=False)

estimatedMean = np.mean( np.array([ estimatedPos1, estimatedPos2, estimatedPos3, estimatedPos4, estimatedPos5, estimatedPos6, estimatedPos7 ]), axis=0 )

# MSE
micCalibrationError2 = mean_squared_error(LsPositions,estimatedMean)
print('MSE2 : ' + str(micCalibrationError2))