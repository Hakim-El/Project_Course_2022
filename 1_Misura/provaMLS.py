import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
from scipy.signal import max_len_seq
from numpy.fft import fft, ifft, fftshift, fftfreq


# dispositivo INPUT e OUTPUT
sd.default.device = [0,1]
sd.default.channels = 2  #1 channel input


# INPUT SIGNAL GENERATION

fs = 44100  

# Maximum length signal MLS (pseudo-random signal)
orderMLS = 15; # order of the mls signal
#sizeMLS = 2^orderMLS-1; # samples

MLS = max_len_seq(orderMLS)[0]*2-1     #just the first array, # +1 and -1
mls = max_len_seq(orderMLS)[0]    # 0 and 1 , binary convention

#PLOTS

#MLS signal 
plt.plot(MLS)
plt.show()


spec = fft(MLS)
N = len(MLS)
plt.plot(fftshift(fftfreq(N)), fftshift(np.abs(spec)), '.-')
plt.margins(0.1, 0.1)
plt.grid(True)
plt.show()


#circular aurocorrelation od an MLS is an impulse (Delta di Kronecker)

acorrcirc = ifft(spec * np.conj(spec)).real
plt.figure()
plt.plot(np.arange(-N/2+1, N/2+1), fftshift(acorrcirc), '.-')
plt.margins(0.1, 0.1)
plt.grid(True)
plt.show()

#########################
#Linear Autocorrelation
acorr = np.correlate(MLS, MLS, 'full')
plt.figure()
plt.plot(np.arange(-N+1, N), acorr, '.-')
plt.margins(0.1, 0.1)
plt.grid(True)
plt.show()




#PLAY and RECORD SIMULTANEOUSLY 
duration = 5 #[s]

sd.play(MLS*0.7, samplerate = fs)  #OCCHIO A NON FARLO CLIPPARE 
sd.stop()



#RIR: CIRCULAR CROSS-CORRELATION BTW MEASURED OUTPUT AND MLS SIGNAL
