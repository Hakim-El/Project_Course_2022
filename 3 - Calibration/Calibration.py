import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy import interpolate
from RIR_generation import createRir

RIR = createRir() # Create a RIR with Pyroomacoustics (See RIR_Generation file)

#Function for finding the direct path of the RIR's (Calibration function)
def find_directPath(this_rir, top_peaks=15):
    this_rir = np.abs(this_rir)     #It computes the absolute value of the RIR to avoid that the first peak is negative
    peaks, _ = find_peaks(this_rir)
    nHighest = (this_rir[peaks]).argsort()[::-1][:top_peaks] # takes the arg of the 15 biggest peaks
    dp = np.sort((peaks[nHighest]))[:1]                      # takes the first (in time) of the 15 biggest peaks
    return dp[0]                                                # dp is the sample the first biggest peak

#Function to compute the distance between two devices through RIR's measurement (Calibration function)
def compute_distance(RIR,fs,c=343,interp_factor = 2, do_interpolation = True):
    interp_factor = interp_factor
    do_interpolation = do_interpolation
    if do_interpolation:
        this_rir = abs(RIR)
        sample_ax = np.arange(0, this_rir.shape[0])
        f = interpolate.interp1d(sample_ax, this_rir, kind='quadratic')
        sample_ax_new = np.arange(0, this_rir.shape[0] - 1, 1/interp_factor)
        dp = find_directPath(f(sample_ax_new))
        distance = (dp/interp_factor)*(1/fs) * c
    else:
        this_rir = abs(RIR)
        dp = find_directPath(this_rir)
        distance = dp*(1/fs) * c        # removed 1/interp_factor when not doing interpolation
    return distance

    # compute distance is not very accurate with pyroom acoustics. Need to try with home simulation