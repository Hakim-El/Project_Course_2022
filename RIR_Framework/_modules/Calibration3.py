from turtle import position
import numpy as np
import scipy.io as sio
from scipy.signal import find_peaks
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.optimize import minimize
from scipy import interpolate


def obj_function(x, positions, toa, buffer, ndim=3):
    if buffer:
        aux = np.reshape(x[:-1], (-1, ndim))
        fun = np.linalg.norm(cdist(positions[:, :ndim], aux[:, :ndim]) - (toa - x[-1]), ord='fro')
    else:
        aux = np.reshape(x, (-1, ndim))
        fun = np.linalg.norm(cdist(positions[:, :ndim], aux[:, :ndim]) - toa, ord='fro')
    return fun


# %% FUNCTIONS
def find_position(positions, toa, positions_bounds, buffer=True, ndim=3, max_buffer=None):
    # bnds = [[None, None], ] * (ndim*toa.shape[1])
    if ndim == 3:
        bnds = positions_bounds * (toa.shape[1])
    else:
        bnds = positions_bounds[:2][:] * (toa.shape[1])

    x0 = np.tile(positions[0, :ndim], (1, toa.shape[1]))
    if buffer:
        x0 = np.append(x0, 0.)
        bnds.append([0, max_buffer])

    bnd = tuple(tuple(x) for x in bnds)

    res = minimize(obj_function, x0, method='SLSQP', bounds=bnd, args=(positions, toa, buffer))
    if ndim is 3:
        if buffer:
            return res.x
        else:
            xTmp = np.empty(shape=(res.x.shape[0] + 1,))
            xTmp[:-1] = res.x
            xTmp[-1] = 0.
            return xTmp
    else:
        if buffer:
            xTmp = np.reshape(res.x[:-1], (-1, 2))
            xTmp = np.concatenate((xTmp, np.zeros(shape=(xTmp.shape[0], 1))), axis=1)
            xTmp = xTmp.ravel()
            xTmp = np.concatenate((xTmp, res.x[-1]), axis=0)
        else:
            xTmp = np.reshape(res.x, (-1, 2))
            xTmp = np.concatenate((xTmp, np.zeros(shape=(xTmp.shape[0], 1))), axis=1)
            xTmp = xTmp.ravel()
            xTmp = np.concatenate((xTmp, 0), axis=0)
        return xTmp


def find_directPath(this_rir, top_peaks=15):
    this_rir = np.abs(this_rir)
    peaks, _ = find_peaks(this_rir)
    nHighest = (this_rir[peaks]).argsort()[::-1][:top_peaks]
    dp = np.sort((peaks[nHighest]))[:1]
    return dp


def calibrate(rir, fs, position_type: str, positions, max_buffer: float,
              positions_bounds, interp_factor: float, do_interpolation: bool = True,
              sound_speed: float = 343, estimate_buffer: bool = True, do_plot: bool = True):
    c = sound_speed
    # %% DATA LOADING
    if position_type is 's':
        rir = np.transpose(rir, (0, 2, 1))

    # %% Position estimation

    # estimatedPosition = np.zeros(shape=(rir.shape[2], 3))
    estimatedBuffer = np.zeros(shape=(rir.shape[2], 1))
    toa = np.zeros(shape=(positions.shape[0], rir.shape[2]))
    for j in range(0, rir.shape[2]):
        for i in range(0, positions.shape[0]):

            if do_interpolation:
                this_rir = rir[:, i, j]
                sample_ax = np.arange(0, this_rir.shape[0])
                f = interpolate.interp1d(sample_ax, this_rir, kind='quadratic')
                sample_ax_new = np.arange(0, this_rir.shape[0] - 1, 1 / interp_factor)
                dp = find_directPath(f(sample_ax_new))
            else:
                this_rir = rir[:, i, j]
                dp = find_directPath(this_rir)

            toa[i, j] = (dp / interp_factor) * (1 / fs) * c

    tmp = find_position(positions, toa, positions_bounds, buffer=estimate_buffer, ndim=3, max_buffer=max_buffer * c)
    estimatedPosition = np.reshape(tmp[:-1], (-1, 3))
    estimatedBuffer = tmp[-1]

    # %% Plot Calibration Result

    if do_plot:
        fig = plt.figure()
        fig.set_tight_layout(False)
        # ax = fig.add_subplot(111, projection='3d')
        ax = Axes3D(fig)
        ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='b', marker='o')
        ax.scatter(estimatedPosition[:, 0], estimatedPosition[:, 1], estimatedPosition[:, 2], c='r', marker='^')
        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')
        ax.set_xlim3d(positions_bounds[0][0], positions_bounds[0][1])
        ax.set_ylim3d(positions_bounds[1][0], positions_bounds[1][1])
        ax.set_zlim3d(positions_bounds[2][0], positions_bounds[2][1])
        plt.show()

        # passare come argomento di input measure method e measure name per decidere dove salvare il plot
        if measureMethod == 1:
            fig.savefig('SineSweepMeasures/{}/MicCalibrationGraph.png'.format(measureName), bbox_inches='tight')
        else:
            fig.savefig('MLSMeasures/{}/MicCalibrationGraph.png'.format(measureName))

    return estimatedPosition, estimatedBuffer
