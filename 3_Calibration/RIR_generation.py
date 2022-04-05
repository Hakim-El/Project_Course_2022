import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve
import IPython
import pyroomacoustics as pra

def createRir(RIRlen):

    #corners = np.array([[0,0], [0,3], [5,3], [5,1], [3,1], [3,0]]).T  # [x,y]
    corners = np.array([[0,0], [0,10], [10,10], [10,0]]).T  # [x,y]

    #fig, ax = room.plot()
    #ax.set_xlim([-1, 6])
    #ax.set_ylim([-1, 4])

    # specify signal source
    fs = 44100
    signal = pra.experimental.signals.exponential_sweep(10, fs, f_lo=0.0, f_hi=None, fade=None, ascending=False)
    #fs, signal = wavfile.read("arctic_a0010.wav")

    # set max_order to a low value for a quick (but less accurate) RIR
    room = pra.Room.from_corners(corners, fs=fs, max_order=3, materials=pra.Material(0.2, 0.15), ray_tracing=False, air_absorption=True)
    room.extrude(4.)

    # Set the ray tracing parameters
    #room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)

    # add source and set the signal to WAV file content
    room.add_source([4., 4., 1.5], signal=signal, delay=0.001)
    room.add_source([5., 8., 1.5], signal=signal, delay=0.001)
    room.add_source([8., 6., 1.5], signal=signal, delay=0.001)



    # add two-microphone array
    R = np.array([5., 5., 1.5])  # [[x], [y], [z]]
    room.add_microphone(R)

    # compute image sources
    room.image_source_model()

    # visualize 3D polyhedron room and image sources
    #fig, ax = room.plot(img_order=3)
    #fig.set_size_inches(18.5, 10.5)

    # compute RIR
    room.compute_rir()

    data = np.zeros((RIRlen,3))

    for i in np.arange(0,3):
        data[:,i] = room.rir[0][i][:RIRlen]

    return data #returns the Impulse response from the first mic

