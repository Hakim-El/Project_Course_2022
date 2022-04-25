import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve
import IPython
import pyroomacoustics as pra

# Creates a simulation of a RIR with 4 Loudspeakers and 1 mic at determined positions
# Used for testing the calibration algorithm
# Predetermined room shape for testing: x = 5m , y = 6m for the 2D case, z = 3m for 3D

knownPos2D = np.array([[1.2, 4.6],
                       [0.7, 1.2],
                       [2.2, 5.3],
                       [4.7, 3.7]])

knownPos3D = np.array([[1.2, 4.6, 1.5],
                       [0.7, 1.2, 1.5],
                       [2.2, 5.3, 1.5],
                       [4.7, 3.7, 1.5]])

def createRir(knownPos, calType, delayType, xlim=5, ylim=6, zlim=3, fs=44100, RIRlen=1332):

    # The desired reverberation time and dimensions of the room
    rt60 = 0.5  # seconds

    # We invert Sabine's formula to obtain the parameters for the ISM simulator
    e_absorption, max_order = pra.inverse_sabine(rt60, [xlim,ylim,zlim])

    corners = np.array([[0,0], [0,ylim], [xlim,ylim], [xlim,0]]).T  # [x,y]

    #fig, ax = room.plot()
    #ax.set_xlim([-1, 6])
    #ax.set_ylim([-1, 4])

    # specify signal source
    signal = pra.experimental.signals.exponential_sweep(10, fs, f_lo=0.0, f_hi=None, fade=None, ascending=False)

    # set max_order to a low value for a quick (but less accurate) RIR
    room = pra.Room.from_corners(corners, fs=fs, max_order=max_order, materials=pra.Material(e_absorption), ray_tracing=False, air_absorption=True)
    
    if calType == 2 :
        room.extrude(zlim)

    # Set the ray tracing parameters
    #room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)

    # add source and set the signal to WAV file content
    knownPos = np.asarray(knownPos)
    outputChannels = knownPos.shape[0]

    if delayType == 1:
        for i in range(0,outputChannels):
            room.add_source(knownPos[i,:], signal=signal, delay=1.3)
    else:
        for i in range(0,outputChannels):
            room.add_source(knownPos[i,:], signal=signal, delay=0)


    # add two-microphone array
    if calType==1:
        R = np.array([1.2, 2.0])  # [[x], [y], [z]]
        room.add_microphone(R)
    else:
        R = np.array([1.2, 2.0, 1.5])
        room.add_microphone(R)

    # compute image sources
    room.image_source_model()

    # visualize 3D polyhedron room and image sources
    #fig, ax = room.plot(img_order=3)
    #fig.set_size_inches(18.5, 10.5)

    # compute RIR
    room.compute_rir()

    data = np.zeros((RIRlen,outputChannels))

    for i in np.arange(0,4):
        data[:RIRlen,i] = room.rir[0][i][:RIRlen]

    return data #returns the Impulse response from the first mic
