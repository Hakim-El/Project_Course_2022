import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
from scipy.signal import max_len_seq
from numpy.fft import fft, ifft, fftshift, fftfreq


# dispositivo INPUT e OUTPUT
sd.default.device = [0,1]
sd.default.channels = 1  #1 channel input


# INPUT SIGNAL GENERATION

fs = 44100  

# Maximum length signal MLS (pseudo-random signal)
orderMLS = 15; # order of the mls signal
sizeMLS = 2^orderMLS-1; # samples

MLS = max_len_seq(sizeMLS)


#PLAY and RECORD SIMULTANEOUSLY 
duration = 5 #[s]

#myrecording = sd.playrec(MLS, fs, dtype = 'int8')  #OCCHIO A NON FARLO CLIPPARE 
#sd.stop()


#PLOTS
spec = fft(MLS)
N = len(MLS)
plt.plot(fftshift(fftfreq(N)), fftshift(np.abs(spec)), '.-')
plt.margins(0.1, 0.1)
plt.grid(True)
plt.show()



