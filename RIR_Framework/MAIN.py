from turtle import clear
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import minimize
from scipy import interpolate
from scipy.signal import spectrogram
from scipy.io.wavfile import write as wavwrite
import sounddevice as sd

# modules from Sine Sweep measure
import stimulus_SineSweep as stim
import _parseargs_SineSweep as parse
import utils_SineSweep as utils

# modules from Calibration
import Calibration as cal

######### INFORMAZIONI SULLA MISURA DA CHIEDERE ALL'UTENTE

print("Questi sono i tuoi devices audio:\n")
print(sd.query_devices())

print ("\nDigita il numero della lista corrispondente al device audio che vuoi utilizzare in INPUT e premi invio:")
inputDevice = int(input())

print("\nDigita il numero della lista corrispondente al device audio che vuoi utilizzare in OUTPUT e premi invio:")
outputDevice = int(input())

print("\nDigita il numero di canali che vuoi utilizzare in INPUT e premi invio (= numero di microfoni)")
inputChannels = int(input())

print("\nDigita il numero di canali che vuoi utilizzare in OUTPUT e premi invio (= numero di sorgenti/altoparlanti)")
outputChannels = int(input())

print("\nScegli la frequenza di campionamneto a cui vuoi lavorare: \n- 1 -> 44100Hz\n- 2 -> 48000Hz\n- 3 -> 96000Hz\n")
fs_selection = int(input())

if fs_selection == 1 :
    fs = 44100
elif fs_selection == 2 :
    fs = 48000
elif fs_selection == 3 :
    fs = 96000
elif fs_selection != 1 and fs_selection!= 2 and fs_selection != 3 :
    print("\nERRORE!\nScegli la frequenza di campionamneto a cui vuoi lavorare: \n- 1 -> 44100Hz\n- 2 -> 48000Hz\n- 3 -> 96000Hz\n")
    fs_selection = int(input())
    if fs_selection == 1 :
        fs = 44100
    elif fs_selection == 2 :
        fs = 48000
    elif fs_selection == 3 :
        fs = 96000

print("\nPRIMA DI PROCEDERE: \n - Collega i n microfoni ai primi n canali di input del device audio selezionato \n - Collega le m sorgenti/altoparlanti ai primi m canali di output del device audio selezionato\n \nDopo aver collegato tutto, premi un tasto qualsiasi e digita invio per andare avanti...")
input()

print("\nScegli il metodo di misura: \n- 1 -> SineSweep\n- 2 -> MLS\n")
recMethod = int(input())

if recMethod != 1 and recMethod != 2 :
   print("\nERRORE!\nScegli il metodo di misura: \n- 1 -> SineSweep\n- 2 -> MLS\n")
   recMethod = int(input())

######### INIZIO CODICE