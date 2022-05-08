import sounddevice as sd
import numpy as np
from scipy import signal
from scipy.signal import fftconvolve

fs = 44100
f1 = 22
f2 = int(fs/2)

w1 = 2*np.pi*f1/fs
w2 = 2*np.pi*f2/fs

amplitude = 0.2
duration = 10
silenceAtStart = 1
silenceAtEnd = 1
repetitions = 1

numSamples = duration*fs
sinsweep = np.zeros(shape = (numSamples,1))
taxis = np.arange(0,numSamples,1)/(numSamples-1)

# for exponential sine sweeping
lw = np.log(w2/w1)
sinsweep = amplitude * np.sin(w1*(numSamples-1)/lw * (np.exp(taxis*lw)-1))

# Find the last zero crossing to avoid the need for fadeout
# Comment the whole block to remove this
#k = np.flipud(sinsweep)
#error = 1
#counter = 0
#while error > 0.001:
#    error = np.abs(k[counter])
#    counter = counter
#k = k[counter::]
#sinsweep_hat = np.flipud(k)
#sinsweep = np.zeros(shape = (numSamples,))
#sinsweep[0:sinsweep_hat.shape[0]] = sinsweep_hat

# the convolutional inverse
envelope = (w2/w1)**(-taxis); # Holters2009, Eq.(9)
invfilter = np.flipud(sinsweep)*envelope
scaling = np.pi*numSamples*(w1/w2-1)/(2*(w2-w1)*np.log(w1/w2))*(w2-w1)/np.pi

# fade-in window. Fade out removed because causes ringing - cropping at zero cross instead
taperStart = signal.tukey(numSamples,0)
taperWindow = np.ones(shape = (numSamples,))
taperWindow[0:int(numSamples/2)] = taperStart[0:int(numSamples/2)]
sinsweep = sinsweep*taperWindow

# Final excitation including repetition and pauses
sinsweep = np.expand_dims(sinsweep,axis = 1)
zerostart = np.zeros(shape = (silenceAtStart*fs,1))
zeroend = np.zeros(shape = (silenceAtEnd*fs,1))
sinsweep = np.concatenate((np.concatenate((zerostart, sinsweep), axis = 0), zeroend), axis=0)
sinsweep = np.transpose(np.tile(np.transpose(sinsweep),repetitions))

Lp = (silenceAtStart + silenceAtEnd + duration)*fs
invfilter = invfilter/amplitude**2/scaling

# recording

inputdevice = 1
outputdevice = 5
inputChannels = 1
outputChannels = 1

sd.default.device = [inputdevice,outputdevice]
sd.default.channels=1
sd.default.samplerate = fs
sd.default.dtype = 'float32'
recorded = sd.playrec(sinsweep, samplerate=fs)
sd.wait()

# Deconvolution

numChans = recorded.shape[1]
tmplen = invfilter.shape[0] + Lp-1
RIRs = np.zeros(shape = (tmplen,numChans))

for idx in range(0,numChans):
    #currentChannel = systemOutput[0:self.repetitions*self.Lp,idx]
    currentChannel = recorded[:,idx]
    # RIRs[:,idx] = fftconvolve(self.invfilter,currentChannel
    # Average over the repetitions - DEPRECATED. Should not be done.
    sig_reshaped = currentChannel.reshape((repetitions,Lp))
    sig_avg = np.mean(sig_reshaped,axis = 0)
    # Deconvolution
    RIRs[:,idx] = fftconvolve(invfilter,sig_avg)
