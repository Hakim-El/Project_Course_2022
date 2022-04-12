import sounddevice as sd
import numpy as np
import matplotlib
import scipy
import os
from RIRmeasure_SineSweep import RIRmeasure_function
from RIRmeasure_MLS import MLSmeasure_function
from Calibration import calculate_Calibration, createDataMatrix, fillDataMatrix

################################  1 - INFORMAZIONI SULLA MISURA DA CHIEDERE ALL'UTENTE ################################

# Lista devices audio
print("Questi sono i tuoi devices audio:\n")
print(sd.query_devices())

# Scelta device di input
print ("\nDigita il numero della lista corrispondente al device audio che vuoi utilizzare in INPUT e premi invio:")
inputDevice = int(input())

# Scelta device di output
print("\nDigita il numero della lista corrispondente al device audio che vuoi utilizzare in OUTPUT e premi invio:")
outputDevice = int(input())

# Scelta numero canali di input (numero microfoni)
print("\nDigita il numero di canali che vuoi utilizzare in INPUT e premi invio (= numero di microfoni)")
inputChannels = int(input())

# Scelta numero canali di output (numero loudspeakers)
print("\nDigita il numero di canali che vuoi utilizzare in OUTPUT e premi invio (= numero di sorgenti/altoparlanti)")
outputChannels = int(input())

# Selezione frequenza di campionamento
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

# Scelta tipo calibrazione 2D o 3D
print("\nVuoi fare una calibrazione in 2D o in 3D?\n \n- Digita 1 per 2D\n- Digita 2 per 3D\n")
print("NB: Per una calibrazione in 2D servono almeno 3 sorgenti per determinare la posizione dei microfoni.\nPer una calibrazione in 3D servono almeno 4 sorgenti per determinare la posizione dei microfoni.")
cal_type = int(input())

if cal_type != 1 and cal_type != 2 :
    print("\nERRORE!")
    print("\nVuoi fare una calibrazione in 2D o in 3D?\n \n- Digita 1 per 2D\n- Digita 2 per 3D\n")
    cal_type = int(input())

if cal_type == 1 :
    print("\nValore asse X (Lunghezza) della stanza [m]:")
    x_axis = float(input())
    print("\nValore asse Y (Larghezza) della stanza [m]:")
    y_axis = float(input())
    z_axis = 0
elif cal_type == 2 :
    print("\nValore asse X (Lunghezza) della stanza [m]:")
    x_axis = float(input())
    print("\nValore asse Y (Larghezza) della stanza [m]:")
    y_axis = float(input())
    print("\nValore asse Z (Altezza) della stanza [m]:")
    z_axis = float(input())

# Stima velocità del suono
print ("\nVuoi impostare manualmente il valore della velocità del suono? Se scegli di non impostarlo, di default c = 343 [m/s]")
print("\n- 1 -> SI\n- 2 -> NO")
x = int(input())

if x == 1:
    print("\nImpostta il valore della temperatura in °C:\n")
    T = float(input())
    c = (331.3 + 0.606*T) # m/s
elif x == 2:
    c = 343 # m/s
elif x != 1 and x != 2:
    print("\nERRORE!\nVuoi impostare manualmente il valore della velocità del suono? Se scegli di non impostarlo, di default c = 343 [m/s]")
    x = int(input())
    if x == 1:
        print("\nImpostta il valore della temperatura in °C:\n")
        T = float(input())
        c = (331.3 + 0.606*T) # m/s
    elif x == 2:
        c = 343 # m/s

# Scelta se tenere in considerazione il delay o no
print("\nVuoi tenere in considerazione il delay di elaborazione dell'algoritmo nel calcolo della RIR e della calibrazione?")
print("\n- 1 -> SI\n- 2 -> NO")
delayType = int(input()) # = 1 delay, = 2 NO delay

if delayType != 1 and delayType != 2 :
    print("\nERRORE!\nVuoi tenere in considerazione il delay di elaborazione dell'algoritmo nel calcolo della RIR e della calibrazione?")
    print("\n- 1 -> SI\n- 2 -> NO")
    delayType = int(input()) # = 1 delay, = 2 NO delay

# Esegui collegamenti dei cavi
print("\nPRIMA DI PROCEDERE: \n - Collega i %d microfoni ai primi %d canali di input del device audio selezionato \n - Collega le %d sorgenti/altoparlanti ai primi %d canali di output del device audio selezionato" %(inputChannels, inputChannels, outputChannels, outputChannels))
print("\nDopo aver collegato tutto, premi invio per andare avanti...")
input()

# Selezione metodo di misura (sinesweep o mls)
print("\nScegli il metodo di misura: \n- 1 -> SineSweep\n- 2 -> MLS\n")
measureMethod = int(input())

if measureMethod != 1 and measureMethod != 2 :
   print("\nERRORE!\nScegli il metodo di misura: \n- 1 -> SineSweep\n- 2 -> MLS\n")
   measureMethod = int(input())

# Posizioni note delle sorgenti 2D e 3D
print("\nInserisci le posizioni note delle %d sorgenti (NB: le posizioni delle sorgenti/altoparlanti sono note, quelle dei microfoni incognite):" %(outputChannels))

if cal_type == 1 :
    knownPos = np.zeros((outputChannels,2))
    for i in range(0,outputChannels) : 
        print("\nPosizione X sorgente/altoparlante %d [m]:" %(i+1))
        knownPos[i,0] = float(input())
        print("\nPosizione Y sorgente/altoparlante %d [m]:" %(i+1))
        knownPos[i,1] = float(input())
elif cal_type == 2 :
    knownPos = np.zeros((outputChannels,3))
    for i in range(0,outputChannels) : 
        print("\nPosizione X sorgente/altoparlante %d [m]:" %(i+1))
        knownPos[i,0] = float(input())
        print("\nPosizione Y sorgente/altoparlante %d [m]:" %(i+1))
        knownPos[i,1] = float(input())
        print("\nPosizione Z sorgente/altoparlante %d [m]:" %(i+1))
        knownPos[i,2] = float(input())

# START
print("\nPremi invio per iniziare la misura.")
input()
print("...\n")

################################  2 - MISURA (SineSweep/MLS) ################################ 

if measureMethod == 1 :
    # Misura SineSweep
    data = createDataMatrix(inputChannels,outputChannels)
    for i in np.arange(1, outputChannels+1) :
        RIRmeasure_function (fs,inputChannels, i, inputDevice, outputDevice)
        data = fillDataMatrix(data,inputChannels,i-1) #da testare con outputChannels>=2
elif measureMethod == 2 :
    # Misura MLS
    for i in np.arange(1, outputChannels+1) :
        MLSmeasure_function (fs,inputChannels, i, inputDevice, outputDevice)
    #print("\nLa MLS ancora non l'abbiamo fatta...\n")
    #exit()

################################ 3 - CALIBRAZIONE E SALVATAGGIO DEI DATI E DEI PLOT ################################ 

# Shows also the results and plot of the calibration
#calculate_Calibration(data, inputChannels, outputChannels, cal_type, delayType, measureMethod, c, fs, knownPos, x_axis, y_axis, z_axis)

# END