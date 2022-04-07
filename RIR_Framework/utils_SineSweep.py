import os
from scipy.io.wavfile import write as wavwrite
import numpy as np
import sounddevice as sd
import MAIN as m

#--------------------------
def record(testsignal,fs,inputChannels, outputChannels):

# Selezione device audio di input e output
    sd.default.device = [m.inputDevice,m.outputDevice] #[input, output]
# Selezione canali da utilizzare in input e in output
    sd.default.channels = [m.inputChannels,m.outputChannels] #[input, output]
    print(sd.query_devices())
   
    sd.default.samplerate = m.fs
    sd.default.dtype = 'float32'
   # print("Input channels:",  inputChannels)
   # print("Output channels:", outputChannels)

    # Start the recording
    recorded = sd.playrec(testsignal, samplerate=fs)
    sd.wait()

    return recorded

#--------------------------
def saverecording(RIR, RIRtoSave, testsignal, recorded, fs):

        dirflag = False
        counter = 1
        dirname = 'Sine_Sweep_Recordings/Measure_1'
        while dirflag == False:
            if os.path.exists(dirname):
                counter = counter + 1
                dirname = 'Sine_Sweep_Recordings/Measure_' + str(counter)
            else:
                os.mkdir(dirname)
                dirflag = True

        # Saving the RIRs and the captured signals
        np.save(dirname+ '/RIR.npy',RIR)
        np.save(dirname+ '/RIRac.npy',RIRtoSave)
        wavwrite(dirname+ '/sigtest.wav',fs,testsignal)

        for idx in range(recorded.shape[1]):
            wavwrite(dirname+ '/sigrec' + str(idx+1) + '.wav',fs,recorded[:,idx])
            wavwrite(dirname+ '/RIR' + str(idx+1) + '.wav',fs,RIR[:,idx])

        # Save in the recorded/lastRecording for a quick check
        np.save('Sine_Sweep_Recordings/lastRecording/RIR.npy',RIR)
        np.save( 'Sine_Sweep_Recordings/lastRecording/RIRac.npy',RIRtoSave)
        wavwrite( 'Sine_Sweep_Recordings/lastRecording/sigtest.wav',fs,testsignal)
       # for idx in range(recorded.shape[1]):
        #    wavwrite('sigrec' + str(idx+1) + '.wav',fs,recorded[:,idx])
         #   wavwrite(dirname+ '/RIR' + str(idx+1) + '.wav',fs,RIR[:,idx])


        print('Success! Recording saved in directory ' + dirname)
