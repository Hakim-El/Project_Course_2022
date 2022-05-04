from email.mime import audio
import tkinter as tk
import sounddevice as sd
import scipy
import numpy as np
import os

################################################## FUNZIONE CHE NON SERVE PIU'########################################################
def printDevices():
    #print (sd.query_devices())
    deviceWindow = tk.Tk()
    deviceWindow.title("Audio Devices List") # titolo
    #deviceWindow.geometry("300x350")
    devices = sd.query_devices()
    counter = 0

    for i in devices:
        frame = tk.Frame(master=deviceWindow)
        tk.Label(frame, text=counter).pack(side=tk.LEFT)
        tk.Label(frame, text=devices[counter]['name']).pack(side=tk.LEFT)
        tk.Label(frame, text=' - IN  :  {}'.format(devices[counter]['max_input_channels'])).pack(side=tk.LEFT)
        tk.Label(frame, text=' - OUT  :  {}'.format(devices[counter]['max_output_channels'])).pack(side=tk.LEFT)
        frame.pack()
        counter += 1
######################################################################################################################################

# CREA MAIN WINDOW
mainWindow = tk.Tk()
mainWindow.title("Automatic RIR Measurement System") # titolo
mainWindow.geometry("900x640") # dimensioni
mainWindow.config(bg='#36454f') # colore

# 1 - Selezione Audio Device di Input
inputDeviceLabel = tk.Label(mainWindow, text="Select Input Audio Device",fg='#36454f')
inputDeviceLabel.place(x=10, y=10)

soundDevicesListInput = sd.query_devices()
variableInputDev = tk.StringVar(mainWindow)
variableInputDev.set('- input AudioDevice -')
opt1 = tk.OptionMenu(mainWindow, variableInputDev, *soundDevicesListInput)
opt1.place(x=10, y=40)

# 2 - Selezione Audio Device di Output
outputDeviceLabel = tk.Label(mainWindow, text="Select Output Audio Device",fg='#36454f')
outputDeviceLabel.place(x=10, y=90)

soundDevicesListOutput = sd.query_devices()
variableOutputDev = tk.StringVar(mainWindow)
variableOutputDev.set('- output AudioDevice -')
opt2 = tk.OptionMenu(mainWindow, variableOutputDev, *soundDevicesListOutput)
opt2.place(x=10, y=120)

# 3 - Selezione numero canali Input
inputChannelLabel = tk.Label(mainWindow, text="Select the number of Input Channles (Microphones)",fg='#36454f')
inputChannelLabel.place(x=300, y=10)

InputDevicesListInputCh = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
variableInputCh = tk.StringVar(mainWindow)
variableInputCh.set('- number of inputs -')
opt3 = tk.OptionMenu(mainWindow, variableInputCh, *InputDevicesListInputCh)
opt3.place(x=300, y=40)

# 4 - Selezione numero canali Output
outputChannelLabel = tk.Label(mainWindow, text="Select the number of Output Channels (Loudspeakers)",fg='#36454f')
outputChannelLabel.place(x=300, y=90)

InputDevicesListOutputCh = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
variableOutputCh = tk.StringVar(mainWindow)
variableOutputCh.set('- number of outputs -')
opt4 = tk.OptionMenu(mainWindow, variableOutputCh, *InputDevicesListOutputCh)
opt4.place(x=300, y=120)

## Istruzioni Collegamento 1
istructions1 = tk.Label(mainWindow, text="ATTENTION!\nNumber of Inputs and outputs must be coherent\nwith the selected audio devices",fg='#36454f')
istructions1.place(x=300, y=170)
## Istruzioni Collegamento 2
istructions2 = tk.Label(mainWindow, text="Connect the selected number n of\nmicrophones to the first n input channels\nof the selected input device\n\nConnect the selected number m of\nloudspeakers to the first m output channels\nof the selected output device", fg='#36454f')
istructions2.place(x=10, y=170)

# 5 - Selezione tipo di misura
measureTypelLabel = tk.Label(mainWindow, text="Type of measure",fg='#36454f')
measureTypelLabel.place(x=660, y=10)

InputDevicesListMeasure = ['SineSweep', 'MLS','PyRoomAcoustics simulation']
variableMeasure = tk.StringVar(mainWindow)
variableMeasure.set('- select -')
opt5 = tk.OptionMenu(mainWindow, variableMeasure, *InputDevicesListMeasure)
opt5.place(x=660, y=40)

# 6 - Selezione Sampling Frequency
frequencyLabel = tk.Label(mainWindow, text="Sampling Frequency [Hz]",fg='#36454f')
frequencyLabel.place(x=660, y=90)

InputDevicesListFreq = [44100, 48000,96000]
variableFreq = tk.StringVar(mainWindow)
variableFreq.set('- select -')
opt6 = tk.OptionMenu(mainWindow, variableFreq, *InputDevicesListFreq)
opt6.place(x=660, y=120)

# 7 - Selezione tipo di calibrazione
calibrationLabel = tk.Label(mainWindow, text="Calibration Type",fg='#36454f')
calibrationLabel.place(x=660, y=170)

InputDevicesListCal = ['2D calibration', '3D calibration']
variableCal = tk.StringVar(mainWindow)
variableCal.set('- none -')
opt7 = tk.OptionMenu(mainWindow, variableCal, *InputDevicesListCal)
opt7.place(x=660, y=200)

# 8 - Delay o no Delay
delayLabel = tk.Label(mainWindow, text="Delay estimation type",fg='#36454f')
delayLabel.place(x=660, y=250)

InputDevicesListDelay = ['Delay estimation', 'NO Delay estimation']
variableDelay = tk.StringVar(mainWindow)
variableDelay.set('- select -')
opt8 = tk.OptionMenu(mainWindow, variableDelay, *InputDevicesListDelay)
opt8.place(x=660, y=280)

# 9 - Sound Speed estimation
soundSpeedLabel = tk.Label(mainWindow, text="Sound Speed estimation",fg='#36454f')
soundSpeedLabel.place(x=660, y=330)

InputDevicesListSoundSpeed = ['Set default value (343 [m/s])', 'Insert temperature in °C below']
variableSoundSpeed = tk.StringVar(mainWindow)
variableSoundSpeed.set('- select -')
opt9 = tk.OptionMenu(mainWindow, variableSoundSpeed, *InputDevicesListSoundSpeed)
opt9.place(x=660, y=360)
T = tk.Entry(mainWindow, width=5)
T.place(x=660, y=390)

if variableSoundSpeed.get() == 'Set default value (343 [m/s])':
    speed = 343
elif variableSoundSpeed.get() == 'Insert temperature in °C below':
    speed = (331.3 + 0.606*T) # m/s

# 10 - Nome della misura -> Serve per dopo
measureNameLabel = tk.Label(mainWindow, text="Insert the name of the measue below\nwithout spaces between words",fg='#36454f')
measureNameLabel.place(x=660, y=440)

measureName = tk.Entry(mainWindow, width=22)
measureName.place(x=660, y=490)

# 11 - Dimensioni della stanza
def printRoomDimension():
    dimension2DWindow = tk.Tk()
    dimension2DWindow.title("Room Dimensions") # titolo
    dimension2DWindow.geometry("270x128") # dimensioni
    dimension2DWindow.config(bg='#36454f') # colore

    if variableCal.get() == '2D calibration' :
        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:')
        xAxisLabel.place(x=10, y=10)
        x_axis = tk.Entry(dimension2DWindow, width=5)
        x_axis.place(x=200, y=10)

        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:')
        yAxisLabel.place(x=10, y=50)
        y_axis = tk.Entry(dimension2DWindow, width=5)
        y_axis.place(x=200, y=50)

        z_axis = 0

    elif variableCal.get() == '3D calibration':
        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:')
        xAxisLabel.place(x=10, y=10)
        x_axis = tk.Entry(dimension2DWindow, width=5)
        x_axis.place(x=200, y=10)
        
        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:')
        yAxisLabel.place(x=10, y=50)
        y_axis = tk.Entry(dimension2DWindow, width=5)
        y_axis.place(x=200, y=50)
       
        zAxisLabel = tk.Label(dimension2DWindow, text='Insert room Z dimension [m]:')
        zAxisLabel.place(x=10, y=90)
        z_axis = tk.Entry(dimension2DWindow, width=5)
        z_axis.place(x=200, y=90)

    elif variableCal.get() == '- none -':
        errDimLabel = tk.Label(dimension2DWindow, text='Select a Calibration Type before')
        errDimLabel.place(x=10, y=10)

roomDimensionButton = tk.Button(mainWindow, text="CLICK HERE to insert Room Dimensions", command = printRoomDimension, fg='#36454f')
roomDimensionButton.place(x=300, y=230)

# 12 - Posizione Loudspeakers -> TO DO
def printLoudspeakerPosition():
    var_i = int(variableOutputCh.get())
    dimension2DWindow = tk.Tk()
    dimension2DWindow.title("Loudspeakers Known Positions") # titolo
    dimension2DWindow.geometry("270x128") # dimensioni
    dimension2DWindow.config(bg='#36454f') # colore

    if variableCal.get() == '2D calibration' :
        for i in range(var_i):
            tk.Label(dimension2DWindow, text= "Loudspeaker " +str(i+1) +" Position").pack()
    elif variableCal.get() == '3D calibration' :
        for i in range(var_i):
            tk.Label(dimension2DWindow, text= "Loudspeaker " +str(i+1) +" Position").pack()
    else:
        errDimLabel2 = tk.Label(dimension2DWindow, text='Select a Calibration Type before')
        errDimLabel2.place(x=10, y=10)
            
loudspeakerPositionButton = tk.Button(mainWindow, text="CLICK HERE to insert known Loudspeaker positions", command = printLoudspeakerPosition, fg='#36454f')
loudspeakerPositionButton.place(x=300, y=260)       

# 13 - START MEASURE -> TO DO
# Lista di variabili con il nome dello script main
inputChannels = variableInputCh.get()
outputChannels = variableOutputCh.get()
fs = variableFreq.get()
# c = speed

if variableCal.get() == '2D calibration':
    cal_type = 1
elif variableCal.get() == '3D calibration':
    cal_type = 2

if variableDelay.get() == 'Delay estimation':
    delayType = 1
elif variableDelay.get() == 'NO Delay estimation':
    delayType = 2

if variableMeasure.get() == 'SineSweep':
    measureMethod = 1
elif variableMeasure.get() == 'MLS':
    measureMethod = 2
elif variableMeasure.get() == 'PyRoomAcoustics simulation':
    measureMethod = 3

# Creazione file di testo con i dati della misura

# Funzioni da eseguire per fare la misura

# pulsante START

buttonStart = tk.Button(mainWindow, height=4, width=10, text="START MEASURE", fg='#36454f') # Inserisci command = funzione main tra text e fg per far partire misura
buttonStart.place(x=700, y=540)

# 14 - Print Posizione Microfoni stimata -> TO DO
micPositionPrintLabel = tk.Label(mainWindow, text="MICROPHONES POSITION ESTIMATION PLOT",fg='#36454f')
micPositionPrintLabel.place(x=10, y=310)

mainWindow.mainloop()

# END