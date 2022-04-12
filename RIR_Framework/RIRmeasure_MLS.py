import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
from scipy.signal import max_len_seq
from numpy.fft import fft, ifft, fftshift, fftfreq


def MLSmeasure_function (fs,inputChannels, i, inputDevice, outputDevice):
    # Viene fatto tutto dentro questa funzione



    # Salvataggio files RIR
    counter = 1
    dirname = 'MLSMeasures/MeasureLoudspeaker1'
