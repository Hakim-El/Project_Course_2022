import os
import sounddevice as sd
import numpy as np
from matplotlib import pyplot as plt

# Modules
import _modules.SineSweep_stimulus as stim
import _modules.SineSweep_parseargs as parse
import _modules.SineSweep_utils as utils

# function to measure and compute a Sine Sweep RIR trhough the desired audio devices and channels 
def RIRmeasure_function (fs, inputDevice, outputDevice, measureName, input_mapping, output_mapping, latency=0):
    # --- Parse command line arguments and check defaults
    flag_defaultsInitialized = parse._checkdefaults()
    args = parse._parse()
    parse._defaults(args)
    
    # -------------------------------

    if flag_defaultsInitialized == True:

        if args.listdev == True:

           # print(sd.query_devices())
            sd.check_input_settings()
            sd.check_output_settings()
            print("Default input and output device: ", sd.default.device )

        elif args.defaults == True:
            aa = np.load('_data/defaults.npy', allow_pickle = True).item()
            for i in aa:
                print (i + " => " + str(aa[i]))

        elif args.setdev == True:

            sd.default.device[0] = args.inputdevice
            sd.default.device[2] = args.outputdevice
            sd.check_input_settings()
            sd.check_output_settings()
            print(sd.query_devices())
            print("Default input and output device: ", sd.default.device )
            print("Sucessfully selected audio devices. Ready to record.")
            parse._defaults(args)

        elif args.test == True:

            deltapeak = stim.test_deconvolution(args)
            plt.plot(deltapeak)
            plt.show()

        else:

            # Create a test signal object, and generate the excitation
            testStimulus = stim.stimulus('sinesweep',fs)
            testStimulus.generate(fs, args.duration, args.amplitude,args.reps,args.startsilence, args.endsilence, args.sweeprange) # sinesweep di 10 secondi
            #testStimulus.generate(fs, 5, args.amplitude,args.reps,args.startsilence, args.endsilence, args.sweeprange) # sinesweep di 5 secondi

            recorded = utils.record(testStimulus.signal,fs, inputDevice, outputDevice, inputMap=input_mapping, outputMap=output_mapping)

            # Deconvolve
            RIR = testStimulus.deconvolve(recorded)

            # Truncate
            # lenRIR = 1.2
            # startId = testStimulus.signal.shape[0] - args.endsilence*fs -1
            # endId = startId + int(lenRIR*fs)
            # # save some more samples before linear part to check for nonlinearities
            # startIdToSave = startId - int(fs/2)
            # RIRtoSave = RIR[startIdToSave:endId,:]
            # RIR = RIR[startId:endId,:]

            RIRtoSave = RIR[RIR.shape[0]//2:,:]
            RIRtoSave = RIRtoSave[latency:,:]

            # Save recordings and RIRs
            utils.saverecording(RIR, RIRtoSave, testStimulus.signal, recorded, fs, measureName, output_mapping)

# create the RIR matrix that will contain all the RIRs of the measurement
def createDataMatrix(nMics, nLS):
    lastRecording = np.load('SineSweepMeasures/_lastMeasureData_/RIR.npy')
    RIRlength = lastRecording.shape[0]
    data = np.zeros((RIRlength,nMics,nLS))
    return data

# fill that matrix with the last measured data
def fillDataMatrix(data, nMics, nLS):
    lastRecording = np.load('SineSweepMeasures/_lastMeasureData_/RIR.npy')
    for i in np.arange(0,nMics):
        data[:,i,nLS-1] = lastRecording[:,i]
    return data
    