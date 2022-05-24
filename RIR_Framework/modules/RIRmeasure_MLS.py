from cmath import sqrt
from turtle import end_fill
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
from scipy.signal import max_len_seq
from numpy.fft import fft, ifft
from scipy.io.wavfile import write as wavwrite
import os

def MLSmeasure_function (fs,inputChannels, outputChannels, inputDevice, outputDevice, measureName, latency=0):
    # Viene fatto tutto dentro questa funzione
    # Generazione del segnale
    orderMLS = 16
    mls = max_len_seq(orderMLS)[0]*2-1     # just the first array, # +1 and -1
    #mls = max_len_seq(orderMLS)[0]        # binary sequence 0 and 1
    #mls = mls*sqrt(2)                # clip it to the range [-sqrt(2) , sqrt(2)] for 3dB headroom

    # AGGIUNGERE 1S DI SILENZIO PRIMA E DOPO
    duration = fs
    zeropad = np.zeros(duration)
    mlsPadded = np.zeros(len(mls)+2*len(zeropad))
    mlsPadded[:len(zeropad)] = zeropad
    mlsPadded[len(zeropad):len(zeropad)+len(mls)] = mls
    mlsPadded[len(zeropad)+len(mls):] = zeropad

    # Selezione device audio di input e output
    sd.default.device = [inputDevice,outputDevice] #[input, output]
    # Selezione canali da utilizzare in input e in output
    sd.default.channels = [inputChannels,outputChannels] #[input, output]
    sd.default.samplerate = fs
    sd.default.dtype = 'float32'

    # perform the average of N recorded mls signals to reduce the effect of noise
    averageN = 3

    # tempRec will contain the 1D arrays of all the mic signals for easier averaging
    tempRec = np.zeros((len(mlsPadded)*inputChannels,averageN)) 

    for idx in np.arange(0,averageN):
        recordedMLS = sd.playrec(mlsPadded, samplerate=fs,dtype='float32', output_mapping=[outputChannels])
        sd.wait()
        tempRec[:,idx] = np.reshape(recordedMLS,recordedMLS.shape[0]*recordedMLS.shape[1],order='F') # reshape to a 1D array

    recordedAverage = np.average(tempRec,axis=1)
    averagedMLS = recordedAverage.reshape((recordedMLS.shape[0],recordedMLS.shape[1]),order='F')

    # Deconvoluzione
    tmplen = mlsPadded.shape[0]
    RIR = np.zeros(shape = (tmplen,averagedMLS.shape[1])) 
    for idx in range(0,averagedMLS.shape[1]):
        RIR[:,idx] = ifft(fft(averagedMLS[:,idx]) * np.conj(fft(mlsPadded))).real # circular cross correlation

    # TAGLIO RIR CON LATENZA
    RIR = RIR[latency:,:]

    # Salvataggio files RIR
    dirflag = False
    counter = 0
    dirname = 'MLSMeasures/' + str(measureName)
    while dirflag == False:
        if os.path.exists(dirname):
            counter = counter + 1
            dirname = 'MLSMeasures/' + str(measureName) + '/MeasureLoudspeaker' + str(counter)
        else:
            os.mkdir(dirname)
            dirflag = True

    # Saving the RIRs and the captured signals
    np.save(dirname+ '/RIR.npy',RIR)
    wavwrite(dirname+ '/sigtest.wav',fs,mlsPadded)

    for idx in range(averagedMLS.shape[1]):
        wavwrite(dirname+ '/sigrec_Mic' + str(idx+1) + '.wav',fs,averagedMLS[:,idx])
        wavwrite(dirname+ '/RIR_Mic' + str(idx+1) + '.wav',fs,RIR[:,idx])

    # Save in the MLSMeasures/_lastMeasureData_ for a quick check
    np.save('MLSMeasures/_lastMeasureData_/RIR.npy',RIR)
    wavwrite( 'MLSMeasures/_lastMeasureData_/sigtest.wav',fs,mlsPadded)
    # for idx in range(recordedMLS.shape[1]):
    #    wavwrite('sigrec' + str(idx+1) + '.wav',fs,recordedMLS[:,idx])
    #    wavwrite(dirname+ '/RIR' + str(idx+1) + '.wav',fs,RIR[:,idx])

    #print('Success! Recording saved in directory ' + dirname)