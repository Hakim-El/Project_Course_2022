import numpy as np
import json
from scipy.spatial.distance import cdist
from sklearn.metrics import mean_squared_error
from _modules.Calibration import find_directPath

RIRMatrix1 = np.load('SineSweepMeasures\measureMicrophonesPosition1\RIRMatrix.npy')
RIRMatrix2 = np.load('SineSweepMeasures\measureLoudspeakersPosition1\RIRMatrix.npy')
fs = 96000
c = 323

with open('SineSweepMeasures\measureMicrophonesPosition1/measureData.json', 'r') as openfile:
    estimPos = json.load(openfile)
    estimPosMic = np.asarray(estimPos['Estimated positions'])
    knownPosLSArray = np.asarray(estimPos['Known positions'])

with open('SineSweepMeasures\measureLoudspeakersPosition1/measureData.json', 'r') as openfile:
    estimPos = json.load(openfile)
    estimPosLS = np.asarray(estimPos['Estimated positions'])

CalibDistMatrix = cdist(estimPosMic,estimPosLS)

RIRdistMatrix = np.zeros((15,6))

for i in range(RIRMatrix2.shape[1]):
    for j in range(RIRMatrix2.shape[2]):
        dp = find_directPath(RIRMatrix2[:,i,j])[0]
        dist = (dp/fs)*c
        RIRdistMatrix[i,j] = dist

print(mean_squared_error(CalibDistMatrix,RIRdistMatrix))