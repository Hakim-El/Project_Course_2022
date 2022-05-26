import numpy as np
import sounddevice as sd
from _modules.SineSweep_RIRmeasure import RIRmeasure_function

fs = 96000
inCh = 1
outCh = 1
inputdev = 6
outputdev = 6
measurename = 'loop3'

RIRmeasure_function(fs,inCh,outCh,inputdev,outputdev,measurename)
