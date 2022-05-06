from email.errors import InvalidMultipartContentTransferEncodingDefect
from email.mime import audio
from re import I
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

NInputs = 1
######################################################################################################################################

# CREA MAIN WINDOW
mainWindow = tk.Tk()
mainWindow.title("Automatic RIR Measurement System") # titolo
mainWindow.geometry("900x640") # dimensioni
mainWindow.config(bg='#36454f') # colore

# 1 - Selezione Audio Device di Input
inputDeviceLabel = tk.Label(mainWindow, text="Select Input Audio Device",fg='#36454f')
inputDeviceLabel.place(x=10, y=10)

devicesDict = sd.query_devices()
devicesList = []

for i in np.arange(0,len(devicesDict)):
    name = f"{i} - {devicesDict[i]['name']} - INPUTS: {devicesDict[i]['max_input_channels']} - OUTPUTS:  {devicesDict[i]['max_output_channels']}"
    devicesList.append(name)

def optionChanged(event, *args):
    global NInputs
    i = int(variableInputDev.get()[0])
    NInputs = devicesDict[i]['max_input_channels']
    menu = opt3['menu']
    menu.delete(0,'end')
    for idx in np.arange(1,NInputs+1):
        menu.add_command(label=str(idx), command=lambda nation=idx: variableInputCh.set(nation))

variableInputDev = tk.StringVar(mainWindow)
variableInputDev.set('- input AudioDevice -')
variableInputDev.trace('w', optionChanged)
opt1 = tk.OptionMenu(mainWindow, variableInputDev, *devicesList)
#opt1.bind('<Deactivate>', optionChanged)
opt1.place(x=10, y=40)

# 2 - Selezione Audio Device di Output
outputDeviceLabel = tk.Label(mainWindow, text="Select Output Audio Device",fg='#36454f')
outputDeviceLabel.place(x=10, y=90)

variableOutputDev = tk.StringVar(mainWindow)
variableOutputDev.set('- output AudioDevice -')
opt2 = tk.OptionMenu(mainWindow, variableOutputDev, *devicesList)
opt2.place(x=10, y=120)

# 3 - Selezione numero canali Input
inputChannelLabel = tk.Label(mainWindow, text="Select the number of Input Channels (Microphones)",fg='#36454f')
inputChannelLabel.place(x=300, y=10)

#InputDevicesListInputCh = np.arange(1,NInputs+1)
variableInputCh = tk.StringVar(mainWindow)
variableInputCh.set('- number of inputs -')
opt3 = tk.OptionMenu(mainWindow, variableInputCh, '')
opt3.place(x=300, y=40)

# 4 - Selezione numero canali Output
outputChannelLabel = tk.Label(mainWindow, text="Select the number of Output Channels (Loudspeakers)",fg='#36454f')
outputChannelLabel.place(x=300, y=90)

InputDevicesListOutputCh = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
variableOutputCh = tk.StringVar(mainWindow)
variableOutputCh.set('- number of outputs -')
opt4 = tk.OptionMenu(mainWindow, variableOutputCh, *InputDevicesListOutputCh)
opt4.place(x=300, y=120)

###################### Istruzioni Collegamento 1
#istructions1 = tk.Label(mainWindow, text="ATTENTION!\nNumber of Inputs and outputs must be coherent\nwith the selected audio devices",fg='#36454f')
#istructions1.place(x=300, y=170)

###################### Istruzioni Collegamento 2
istructions2 = tk.Label(mainWindow, text="Connect the selected number n of\nmicrophones to the first n input channels\nof the selected input device\n\nConnect the selected number m of\nloudspeakers to the first m output channels\nof the selected output device", fg='#36454f')
istructions2.place(x=10, y=170)

###################### 5 - Selezione tipo di misura
measureTypelLabel = tk.Label(mainWindow, text="Type of measure",fg='#36454f')
measureTypelLabel.place(x=660, y=10)

InputDevicesListMeasure = ['SineSweep', 'MLS','PyRoomAcoustics simulation']
variableMeasure = tk.StringVar(mainWindow)
variableMeasure.set('- select -')
opt5 = tk.OptionMenu(mainWindow, variableMeasure, *InputDevicesListMeasure)
opt5.place(x=660, y=40)

def getMeasureType():
    global measureMethod
    if variableMeasure.get() == 'SineSweep':
        measureMethod = 1
    elif variableMeasure.get() == 'MLS':
        measureMethod = 2
    elif variableMeasure.get() == 'PyRoomAcoustics simulation':
        measureMethod = 3

###################### 6 - Selezione Sampling Frequency
frequencyLabel = tk.Label(mainWindow, text="Sampling Frequency [Hz]",fg='#36454f')
frequencyLabel.place(x=660, y=90)

InputDevicesListFreq = [44100, 48000,96000]
variableFreq = tk.StringVar(mainWindow)
variableFreq.set('- select -')
opt6 = tk.OptionMenu(mainWindow, variableFreq, *InputDevicesListFreq)
opt6.place(x=660, y=120)

def getFrequency():
    global fs
    fs = int(variableFreq.get())

###################### 7 - Selezione tipo di calibrazione
calibrationLabel = tk.Label(mainWindow, text="Calibration Type",fg='#36454f')
calibrationLabel.place(x=660, y=170)

InputDevicesListCal = ['2D calibration', '3D calibration']
variableCal = tk.StringVar(mainWindow)
variableCal.set('- none -')
opt7 = tk.OptionMenu(mainWindow, variableCal, *InputDevicesListCal)
opt7.place(x=660, y=200)

def getCalibrationType():
    global cal_type
    if variableCal.get() == '2D calibration':
        cal_type = 1
    elif variableCal.get() == '3D calibration':
        cal_type = 2

###################### 8 - Delay o no Delay
delayLabel = tk.Label(mainWindow, text="Delay estimation type",fg='#36454f')
delayLabel.place(x=660, y=250)

InputDevicesListDelay = ['Delay estimation', 'NO Delay estimation']
variableDelay = tk.StringVar(mainWindow)
variableDelay.set('- select -')
opt8 = tk.OptionMenu(mainWindow, variableDelay, *InputDevicesListDelay)
opt8.place(x=660, y=280)

def getDelayType():
    global delayType
    if variableDelay.get() == 'Delay estimation':
        delayType = 1
    elif variableDelay.get() == 'NO Delay estimation':
        delayType = 2

###################### 9 - Sound Speed estimation
soundSpeedLabel = tk.Label(mainWindow, text="Sound Speed estimation",fg='#36454f')
soundSpeedLabel.place(x=660, y=330)

InputDevicesListSoundSpeed = ['Set default value (343 [m/s])', 'Insert temperature in °C below']
variableSoundSpeed = tk.StringVar(mainWindow)
variableSoundSpeed.set('- select -')
opt9 = tk.OptionMenu(mainWindow, variableSoundSpeed, *InputDevicesListSoundSpeed)
opt9.place(x=660, y=360)
t = tk.Entry(mainWindow, width=5)
t.place(x=660, y=390)
T = t.get()

def defineSoundSpeed():
    global c
    if variableSoundSpeed.get() == 'Set default value (343 [m/s])':
        c = 343
    elif variableSoundSpeed.get() == 'Insert temperature in °C below':
        c = (331.3 + 0.606*int(t.get())) # m/s
    else:
        c = 343

###################### 10 - Nome della misura -> Serve per dare nome alla cartella con i dati della misura
measureNameLabel = tk.Label(mainWindow, text="Insert the name of the measue below\nwithout spaces between words",fg='#36454f')
measureNameLabel.place(x=660, y=440)

Name = tk.Entry(mainWindow, width=22)
Name.place(x=660, y=490)

def nameOfMeasure():
    global measureName
    measureName = Name.get()

###################### 11 - Dimensioni della stanza
def printRoomDimension():
    dimension2DWindow = tk.Tk()
    dimension2DWindow.title("Room Dimensions") # titolo
    dimension2DWindow.config(bg='#36454f') # colore

    if variableCal.get() == '2D calibration' :
        dimension2DWindow.geometry("270x130") # dimensioni

        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:')
        xAxisLabel.place(x=10, y=10)
        x_dim = tk.Entry(dimension2DWindow, width=5)
        x_dim.place(x=200, y=10)

        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:')
        yAxisLabel.place(x=10, y=50)
        y_dim = tk.Entry(dimension2DWindow, width=5)
        y_dim.place(x=200, y=50)

        z_dim = tk.StringVar(dimension2DWindow) 
        z_dim.set('0.0')

    elif variableCal.get() == '3D calibration':
        dimension2DWindow.geometry("270x170") # dimensioni

        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:')
        xAxisLabel.place(x=10, y=10)
        x_dim = tk.Entry(dimension2DWindow, width=5)
        x_dim.place(x=200, y=10)
        
        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:')
        yAxisLabel.place(x=10, y=50)
        y_dim = tk.Entry(dimension2DWindow, width=5)
        y_dim.place(x=200, y=50)
       
        zAxisLabel = tk.Label(dimension2DWindow, text='Insert room Z dimension [m]:')
        zAxisLabel.place(x=10, y=90)
        z_dim = tk.Entry(dimension2DWindow, width=5)
        z_dim.place(x=200, y=90)

    elif variableCal.get() == '- none -':
        dimension2DWindow.geometry("270x60") # dimensioni

        errDimLabel = tk.Label(dimension2DWindow, text='Select a Calibration Type before')
        errDimLabel.place(x=10, y=10)

    def getRoomDimensions():
        global x_axis
        global y_axis
        global z_axis

        x_axis = float(x_dim.get())
        y_axis = float(y_dim.get())
        z_axis = float(z_dim.get())
    
    getDimensions = tk.Button(dimension2DWindow, text='Click here to confirm dimemsions', command=getRoomDimensions)

    if variableCal.get() == '2D calibration' :
        getDimensions.place(x=10, y=90)
    elif variableCal.get() == '3D calibration':
        getDimensions.place(x=10, y=130)

roomDimensionButton = tk.Button(mainWindow, text="CLICK HERE to confirm Room Dimensions", command = printRoomDimension, fg='#36454f')
roomDimensionButton.place(x=300, y=230)

# 12 - Posizione Loudspeakers -> TO DO
def printLoudspeakerPosition():
    var_i = int(variableOutputCh.get())
    LoudSpeakerWindow = tk.Tk()
    LoudSpeakerWindow.title("Loudspeakers Known Positions") # titolo
    LoudSpeakerWindow.geometry('%dx%d' %(710, (var_i*100)/2.5)) # dimensioni
    LoudSpeakerWindow.config(bg='#36454f') # colore

    if variableCal.get() == '2D calibration' :
        for i in range(var_i):
            tk.Label(LoudSpeakerWindow, text= "Loudspeaker " +str(i+1) +" Position (X ; Y)").place(x=10, y=11*3.5*i)
            x_pos = tk.Entry(LoudSpeakerWindow, width=5)
            x_pos.place(x=220, y=11*3.5*i)
            y_pos = tk.Entry(LoudSpeakerWindow, width=5)
            y_pos.place(x=290, y=11*3.5*i)

            z_pos = tk.StringVar(LoudSpeakerWindow) 
            z_pos.set('0.0')

    elif variableCal.get() == '3D calibration' :
        for i in range(var_i):
            tk.Label(LoudSpeakerWindow, text= "Loudspeaker " +str(i+1) +" Position (X ; Y ; Z)").place(x=10, y=11*3.5*i)
            x_pos = tk.Entry(LoudSpeakerWindow, width=5)
            x_pos.place(x=230, y=11*3.5*i)
            y_pos = tk.Entry(LoudSpeakerWindow, width=5)
            y_pos.place(x=300, y=11*3.5*i)
            z_pos = tk.Entry(LoudSpeakerWindow, width=5)
            z_pos.place(x=370, y=11*3.5*i)
            
    else:
        errDimLabel2 = tk.Label(LoudSpeakerWindow, text='Select a Calibration Type before')
        errDimLabel2.place(x=10, y=10)

    #def getLoudSpeakersPositions():
    #    global knownPos
    #    global x_pos
    #    global y_pos
    #    global z_pos
    #
    #    if cal_type == 1 :
    #        knownPos = np.zeros((var_i,2))
    #        for i in range(0,var_i) : 
    #            knownPos[i,0] = float(x_pos.get())
    #            knownPos[i,1] = float(y_pos.get())
    #    elif cal_type == 2 :
    #        knownPos = np.zeros((var_i,3))
    #        for i in range(0,var_i) : 
    #            knownPos[i,0] = float(x_pos.get())
    #            knownPos[i,1] = float(y_pos.get())
    #            knownPos[i,2] = float(z_pos.get())
    
    getPositions = tk.Button(LoudSpeakerWindow, text='CLICK HERE to confirm Loudspeaker\nknown positions')
    getPositions.place(x=440, y=10)

loudspeakerPositionButton = tk.Button(mainWindow, text="CLICK HERE to insert known Loudspeaker positions", command = printLoudspeakerPosition, fg='#36454f')
loudspeakerPositionButton.place(x=300, y=260)       

# 13 - START MEASURE BUTTON -> TO DO
# Lista di variabili con il nome dello script main

# Creazione file di testo con i dati della misura

# Funzioni da eseguire per fare la misura

def multipleStartFunctions(): # to set all varaibles
    inputChannels = variableInputCh.get()
    outputChannels = variableOutputCh.get()
    nameOfMeasure()
    defineSoundSpeed()
    getDelayType()
    getCalibrationType()
    getMeasureType()
    getFrequency()
    
    # print all variables on Terminal
    print('\n\n')
    print('Measure Name: %s' %measureName)
    print('Number of Input Channels: %d' %int(inputChannels))
    print('Number of Output Channels: %d' %int(outputChannels))
    print('Measure Type: %d' %measureMethod)
    print('Calibration Type: %d' %cal_type)
    print('Delay Estimation Type: %d' %delayType)
    print('Sampling Frequency [Hz]: %d' %fs)
    print('Sound Speed [m/s]: %.2f' %c)
    print('Room Dimensions X, Y, Z [m]: %.2f, %.2f, %.2f' %(x_axis, y_axis, z_axis))
    print('\n')

buttonStart = tk.Button(mainWindow, height=4, width=10, text="START MEASURE", command=multipleStartFunctions, fg='#36454f') # Inserisci command = funzione main tra text e fg per far partire misura
buttonStart.place(x=700, y=540)

# 14 - Print Posizione Microfoni stimata -> TO DO
micPositionPrintLabel = tk.Label(mainWindow, text="MICROPHONES POSITION ESTIMATION PLOT",fg='#36454f')
micPositionPrintLabel.place(x=10, y=310)

mainWindow.mainloop()

# END