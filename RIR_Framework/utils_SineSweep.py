import os
from scipy.io.wavfile import write as wavwrite
import numpy as np
import sounddevice as sd

#--------------------------

def record(testsignal,fs,inputChannels, outputChannels, inputDevice, outputDevice):

# Selezione device audio di input e output
    sd.default.device = [inputDevice,outputDevice] #[input, output]
# Selezione canali da utilizzare in input e in output
    sd.default.channels = [inputChannels,outputChannels] #[input, output]
    #print(sd.query_devices())
   
    sd.default.samplerate = fs
    sd.default.dtype = 'float32'
   # print("Input channels:",  inputChannels)
   # print("Output channels:", outputChannels)

    # Start the recording
    recorded = sd.playrec(testsignal, samplerate=fs, output_mapping=[outputChannels])
    sd.wait()

    return recorded

#--------------------------

def saverecording(RIR, RIRtoSave, testsignal, recorded, fs, measureName):

        dirflag = False
        counter = 0
        dirname = 'SineSweepMeasures/' + str(measureName)
        while dirflag == False:
            if os.path.exists(dirname):
                counter = counter + 1
                dirname = 'SineSweepMeasures/' + str(measureName) + '/MeasureLoudspeaker' + str(counter)
            else:
                os.mkdir(dirname)
                dirflag = True

        # Saving the RIRs and the captured signals
        #np.save(dirname+ '/RIR.npy',RIR)
        np.save(dirname+ '/RIR.npy',RIRtoSave)
        wavwrite(dirname+ '/sigtest.wav',fs,testsignal)

        for idx in range(recorded.shape[1]):
            wavwrite(dirname+ '/sigrec_Mic' + str(idx+1) + '.wav',fs,recorded[:,idx])
            wavwrite(dirname+ '/RIR_Mic' + str(idx+1) + '.wav',fs,8*RIRtoSave[:,idx])

        # Save in the Sine_Sweep_Measures/_lastMeasureData_ for a quick check
        #np.save('SineSweepMeasures/_lastMeasureData_/RIR.npy',RIR)
        np.save( 'SineSweepMeasures/_lastMeasureData_/RIR.npy',RIRtoSave)
        wavwrite( 'SineSweepMeasures/_lastMeasureData_/sigtest.wav',fs,testsignal)
       # for idx in range(recorded.shape[1]):
        #    wavwrite('sigrec' + str(idx+1) + '.wav',fs,recorded[:,idx])
        #    wavwrite(dirname+ '/RIR' + str(idx+1) + '.wav',fs,RIR[:,idx])

        #print('Success! Recording saved in directory ' + dirname)
