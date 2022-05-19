import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
from scipy.signal import max_len_seq
from numpy.fft import fft, ifft, fftshift, fftfreq
from scipy.io.wavfile import write as wavwrite
import os

def MLSmeasure_function (fs,inputChannels, outputChannels, inputDevice, outputDevice, measureName):
    # Viene fatto tutto dentro questa funzione
    # Generazione del segnale
    orderMLS = 18
    #MLS = max_len_seq(orderMLS)[0]*2-1     # just the first array, # +1 and -1
    mls = max_len_seq(orderMLS)[0]    # 0 and 1 , binary convention

    # Selezione device audio di input e output
    sd.default.device = [inputDevice,outputDevice] #[input, output]
    # Selezione canali da utilizzare in input e in output
    sd.default.channels = [inputChannels,outputChannels] #[input, output]
    sd.default.samplerate = fs
    sd.default.dtype = 'float32'

    recordedMLS = sd.playrec(mls, samplerate=fs, output_mapping=[outputChannels])
    sd.wait()

    recordedMLSreshaped = recordedMLS.reshape(mls.shape)

    # Deconvoluzione
    specRecorded = fft(recordedMLSreshaped)
    specMLS = fft(mls)
    RIR = ifft(specMLS * np.conj(specRecorded)).real # circular cross correlation

    #plt.plot(RIR)
    #plt.show()

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
    #np.save(dirname+ '/RIRac.npy',RIRtoSave)
    wavwrite(dirname+ '/sigtest.wav',fs,mls)

    for idx in range(recordedMLS.shape[1]):
        wavwrite(dirname+ '/sigrec_Mic' + str(idx+1) + '.wav',fs,recordedMLS[:,idx])
        wavwrite(dirname+ '/RIR_Mic' + str(idx+1) + '.wav',fs,RIR[:,idx])

    # Save in the MLSMeasures/_lastMeasureData_ for a quick check
    np.save('MLSMeasures/_lastMeasureData_/RIR.npy',RIR)
    #np.save( 'MLSMeasures/_lastMeasureData_/RIRac.npy',RIRtoSave)
    wavwrite( 'MLSMeasures/_lastMeasureData_/sigtest.wav',fs,mls)
    # for idx in range(recordedMLS.shape[1]):
    #    wavwrite('sigrec' + str(idx+1) + '.wav',fs,recordedMLS[:,idx])
    #    wavwrite(dirname+ '/RIR' + str(idx+1) + '.wav',fs,RIR[:,idx])

    #print('Success! Recording saved in directory ' + dirname)