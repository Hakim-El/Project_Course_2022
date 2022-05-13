import tkinter as tk
from typing import Literal
import sounddevice as sd
import pyroomacoustics
import matplotlib.pyplot as plt
import scipy
import numpy as np
import os
import shutil

from RIRmeasure_SineSweep import RIRmeasure_function
from RIRmeasure_MLS import MLSmeasure_function
from Calibration import calculate_Calibration, createDataMatrix, fillDataMatrix, find_directPath
from RIRsimulation import createRir

###################################################################################################

# CREA MAIN WINDOW
mainWindow = tk.Tk()
mainWindow.title("Automatic RIR Measurement System") # titolo
mainWindow.geometry("980x510") # dimensioni
mainWindow.config(bg='#36454f') # colore

# MAIN WINDOW SPACING
borderSpace1 = tk.Label(mainWindow, text='', bg='#36454f').grid(row=1,rowspan=1)
borderSpace2 = tk.Label(mainWindow, text='', bg='#36454f').grid(column=1, columnspan=1)

verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=2, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=3, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=4, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=5, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=6, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=7, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=8, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=9, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=10, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=11, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=12, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=13, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=14, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=15, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=16, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=17, column=3)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=18, column=3)

verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=2, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=3, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=4, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=5, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=6, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=7, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=8, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=9, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=10, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=11, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=12, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=13, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=14, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=15, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=16, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=17, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=18, column=5)

credits = tk.Label(mainWindow, text='\n\nDeveloped by: Hakim El Achak, Lorenzo Lellini, Jacopo Caucig', font=('Helvetica 11 italic'), bg='#36454f', fg='#000000')
credits.grid(row=17, column=2)

###################### 1 - Selezione Audio Device di Input ######################
inputDeviceLabel = tk.Label(mainWindow, text="1) Select Input Audio Device", bg='#36454f', fg='#f7f7f7')
inputDeviceLabel.grid(row=2, column=2)

devicesDict = sd.query_devices()
devicesList = []

for i in np.arange(0,len(devicesDict)):
    name = f"{i} - {devicesDict[i]['name']} - IN: {devicesDict[i]['max_input_channels']} | OUT:  {devicesDict[i]['max_output_channels']}"
    devicesList.append(name)

def inputChanged(event, *args):
    i = int(variableInputDev.get()[0])
    NInputs = devicesDict[i]['max_input_channels']
    menu = opt3['menu']
    menu.delete(0,'end')
    for idx in np.arange(1,NInputs+1):
        menu.add_command(label=str(idx), command=lambda ch=idx: variableInputCh.set(ch))
    opt1.config(anchor='w')

def outputChanged(event, *args):
    i = int(variableOutputDev.get()[0])
    NOutputs = devicesDict[i]['max_output_channels']
    menu = opt4['menu']
    menu.delete(0,'end')
    for idx in np.arange(1,NOutputs+1):
        menu.add_command(label=str(idx), command=lambda ch=idx: variableOutputCh.set(ch))
    opt2.config(anchor='w')

variableInputDev = tk.StringVar(mainWindow)
variableInputDev.set('- input AudioDevice -')
variableInputDev.trace('w', inputChanged)
opt1 = tk.OptionMenu(mainWindow, variableInputDev, *devicesList)
opt1.config(width=30)
opt1.grid(row=3, column=2)

###################### 2 - Selezione Audio Device di Output ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=4, column=2)
outputDeviceLabel = tk.Label(mainWindow, text="2) Select Output Audio Device", bg='#36454f', fg='#f7f7f7')
outputDeviceLabel.grid(row=5, column=2)

variableOutputDev = tk.StringVar(mainWindow)
variableOutputDev.set('- output AudioDevice -')
variableOutputDev.trace('w', outputChanged)
opt2 = tk.OptionMenu(mainWindow, variableOutputDev, *devicesList)
opt2.config(width=30)
opt2.grid(row=6, column=2)

###################### 3 - Selezione numero canali Input ######################
inputChannelLabel = tk.Label(mainWindow, text="3) Select the number of Input Channels (Microphones)", bg='#36454f', fg='#f7f7f7')
inputChannelLabel.grid(row=2, column=4)

#InputDevicesListInputCh = np.arange(1,NInputs+1)
variableInputCh = tk.StringVar(mainWindow)
variableInputCh.set('- number of inputs -  ')
opt3 = tk.OptionMenu(mainWindow, variableInputCh, '')
opt3.config(width=13)
opt3.grid(row=3, column=4)


###################### 4 - Selezione numero canali   ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=4, column=4)
outputChannelLabel = tk.Label(mainWindow, text="4) Select the number of Output Channels (Loudspeakers)", bg='#36454f', fg='#f7f7f7')
outputChannelLabel.grid(row=5, column=4)

variableOutputCh = tk.StringVar(mainWindow)
variableOutputCh.set('- number of outputs -')
opt4 = tk.OptionMenu(mainWindow, variableOutputCh, '')
opt4.config(width=13)
opt4.grid(row=6, column=4)

###################### Istruzioni Collegamento ######################

def wiringInstructions():
    wiringInstructionsWindow = tk.Tk()
    wiringInstructionsWindow.title("Cable Connections") # titolo
    wiringInstructionsWindow.config(bg='#36454f') # colore

    instructions1 = tk.Label(wiringInstructionsWindow, text='WIRING INSTRUCTIONS', font='Helvetica 16 bold', bg='#36454f', fg='#f7f7f7')
    instructions1.grid(row=2, column=2)
    instructions2 = tk.Label(wiringInstructionsWindow, text="Connect the selected number N of\nmicrophones to the first N input channels\nof the selected input device\n------\nConnect the selected number M of\nloudspeakers to the first M output channels\nof the selected output device\n", bg='#36454f', fg='#f7f7f7')
    instructions2.grid(row=3, column=2)

wiringButton = tk.Button(mainWindow, text='- CLICK HERE FOR WIRING INSTRUCTIONS - ', command=wiringInstructions)
wiringButton.grid(row=9, column=2)

###################### 5 - Selezione tipo di misura ######################
measureTypelLabel = tk.Label(mainWindow, text="5) Type of measure", bg='#36454f', fg='#f7f7f7')
measureTypelLabel.grid(row=2, column=6)

InputDevicesListMeasure = ['SineSweep', 'MLS','PyRoomAcoustics simulation']
variableMeasure = tk.StringVar(mainWindow)
variableMeasure.set('- select -')
opt5 = tk.OptionMenu(mainWindow, variableMeasure, *InputDevicesListMeasure)
opt5.config(width=8)
opt5.grid(row=3, column=6)

###################### 6 - Selezione Sampling Frequency ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=4, column=6)
frequencyLabel = tk.Label(mainWindow, text="6) Sampling Frequency [Hz]", bg='#36454f', fg='#f7f7f7')
frequencyLabel.grid(row=5, column=6)

InputDevicesListFreq = [44100, 48000,96000]
variableFreq = tk.StringVar(mainWindow)
variableFreq.set('- select -')
opt6 = tk.OptionMenu(mainWindow, variableFreq, *InputDevicesListFreq)
opt6.config(width=8)
opt6.grid(row=6, column=6)

###################### 7 - Selezione tipo di calibrazione ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=7, column=6)
calibrationLabel = tk.Label(mainWindow, text="7) Estimation Type", bg='#36454f', fg='#f7f7f7')
calibrationLabel.grid(row=8, column=6)

InputDevicesListCal = ['2D calibration', '3D calibration']
variableCal = tk.StringVar(mainWindow)
variableCal.set('- select -')
opt7 = tk.OptionMenu(mainWindow, variableCal, *InputDevicesListCal)
opt7.config(width=8)
opt7.grid(row=9, column=6)

###################### 8 - Delay o no Delay ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=10, column=6)
delayLabel = tk.Label(mainWindow, text="8) Delay estimation type", bg='#36454f', fg='#f7f7f7')
delayLabel.grid(row=11, column=6)

InputDevicesListDelay = ['Delay estimation', 'NO Delay estimation']
variableDelay = tk.StringVar(mainWindow)
variableDelay.set('- select -     ')
opt8 = tk.OptionMenu(mainWindow, variableDelay, *InputDevicesListDelay)
opt8.grid(row=12, column=6)

###################### 9 - Sound Speed estimation ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=13, column=6)
soundSpeedLabel = tk.Label(mainWindow, text="9) Sound Speed estimation", bg='#36454f', fg='#f7f7f7')
soundSpeedLabel.grid(row=14, column=6)

InputDevicesListSoundSpeed = ['Set default value (343 [m/s])', 'Insert temperature in °C below']
variableSoundSpeed = tk.StringVar(mainWindow)
variableSoundSpeed.set('- select -     ')
opt9 = tk.OptionMenu(mainWindow, variableSoundSpeed, *InputDevicesListSoundSpeed)
opt9.grid(row=15, column=6)
t = tk.Entry(mainWindow, width=5)
t.grid(row=16, column=6)

###################### 10 - Nome della misura ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=18, column=6)
measureNameLabel = tk.Label(mainWindow, text="10) Insert the name of the measure below", bg='#36454f', fg='#f7f7f7')
measureNameLabel.grid(row=8, column=4)
Name = tk.Entry(mainWindow, width=40)
Name.grid(row=9, column=4)

###################### 11 - Dimensioni della stanza ######################
def printRoomDimension():
    dimension2DWindow = tk.Tk()
    dimension2DWindow.title("Room Dimensions") # titolo
    dimension2DWindow.config(bg='#36454f') # colore

    if variableCal.get() == '2D calibration' :
        dimension2DWindow.geometry("270x130") # dimensioni

        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:', bg='#36454f', fg='#f7f7f7')
        xAxisLabel.place(x=10, y=10)
        x_dim = tk.Entry(dimension2DWindow, width=5)
        x_dim.place(x=200, y=10)

        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:', bg='#36454f', fg='#f7f7f7')
        yAxisLabel.place(x=10, y=50)
        y_dim = tk.Entry(dimension2DWindow, width=5)
        y_dim.place(x=200, y=50)

        z_dim = tk.StringVar(dimension2DWindow) 
        z_dim.set('0.0')

    elif variableCal.get() == '3D calibration':
        dimension2DWindow.geometry("270x170") # dimensioni

        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:', bg='#36454f', fg='#f7f7f7')
        xAxisLabel.place(x=10, y=10)
        x_dim = tk.Entry(dimension2DWindow, width=5)
        x_dim.place(x=200, y=10)
        
        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:', bg='#36454f', fg='#f7f7f7')
        yAxisLabel.place(x=10, y=50)
        y_dim = tk.Entry(dimension2DWindow, width=5)
        y_dim.place(x=200, y=50)
       
        zAxisLabel = tk.Label(dimension2DWindow, text='Insert room Z dimension [m]:', bg='#36454f', fg='#f7f7f7')
        zAxisLabel.place(x=10, y=90)
        z_dim = tk.Entry(dimension2DWindow, width=5)
        z_dim.place(x=200, y=90)

    elif variableCal.get() == '- select -':
        dimension2DWindow.geometry("270x60") # dimensioni

        errDimLabel = tk.Label(dimension2DWindow, text='Select a Calibration Type before', bg='#36454f', fg='#f7f7f7')
        errDimLabel.place(x=10, y=10)

    def getRoomDimensions():
        global x_axis
        global y_axis
        global z_axis

        x_axis = float(x_dim.get())
        y_axis = float(y_dim.get())
        z_axis = float(z_dim.get())
    
    getDimensions = tk.Button(dimension2DWindow, text='CLICK HERE to confirm dimemsions', command=getRoomDimensions, fg='#36454f')

    if variableCal.get() == '2D calibration' :
        getDimensions.place(x=10, y=90)
    elif variableCal.get() == '3D calibration':
        getDimensions.place(x=10, y=130)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=10, column=4)
roomDimensionButton = tk.Button(mainWindow, height=1, width=37, text="11) CLICK HERE to insert Room Dimensions", command = printRoomDimension, fg='#36454f')
roomDimensionButton.grid(row=11, column=4)

###################### 12 - Posizione Loudspeakers ######################
def printLoudspeakerPosition():
    var_i = int(variableOutputCh.get())
    LoudSpeakerWindow = tk.Tk()
    LoudSpeakerWindow.title("Loudspeakers Known Positions") # titolo
    LoudSpeakerWindow.geometry('%dx%d' %(810, (8+(var_i*100)/2.5))) # dimensioni
    LoudSpeakerWindow.config(bg='#36454f') # colore

    if variableCal.get() == '2D calibration' :
        global x_pos 
        global y_pos
        global z_pos
        x_pos = []
        y_pos = []
        z_pos = 0
        for i in range(var_i):
            tk.Label(LoudSpeakerWindow, text= "Loudspeaker " +str(i+1) +" Position (X ; Y)",  bg='#36454f', fg='#f7f7f7').place(x=10, y=11*3.5*i)
            x_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            x_pos[i].place(x=220, y=11*3.5*i)
            y_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            y_pos[i].place(x=290, y=11*3.5*i)

    elif variableCal.get() == '3D calibration' :
        x_pos = []
        y_pos = []
        z_pos = []
        for i in range(var_i):
            tk.Label(LoudSpeakerWindow, text= "Loudspeaker " +str(i+1) +" Position (X ; Y ; Z)",  bg='#36454f', fg='#f7f7f7').place(x=10, y=11*3.5*i)
            x_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            x_pos[i].place(x=230, y=11*3.5*i)
            y_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            y_pos[i].place(x=300, y=11*3.5*i)
            z_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            z_pos[i].place(x=370, y=11*3.5*i)
            
    elif variableCal.get() == '- select -':
        errDimLabel2 = tk.Label(LoudSpeakerWindow, text='Select a Calibration Type before', bg='#36454f', fg='#f7f7f7')
        errDimLabel2.place(x=10, y=10)

    def getLoudSpeakersPositions():
        global knownPos
        if variableCal.get() == '2D calibration' :
            knownPos = np.zeros((var_i,2))
            for i in range(0,var_i) : 
                knownPos[i,0] = float(x_pos[i].get())
                knownPos[i,1] = float(y_pos[i].get())
        elif variableCal.get() == '3D calibration' :
            knownPos = np.zeros((var_i,3))
            for i in range(0,var_i) : 
                knownPos[i,0] = float(x_pos[i].get())
                knownPos[i,1] = float(y_pos[i].get())
                knownPos[i,2] = float(z_pos[i].get())
    
    getPositions = tk.Button(LoudSpeakerWindow, text='CLICK HERE to confirm known Loudspeaker positions', command=getLoudSpeakersPositions, fg='#36454f')
    getPositions.place(x=440, y=10)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=12, column=4)
loudspeakerPositionButton = tk.Button(mainWindow,text="12) CLICK HERE to insert known Loudspeaker positions", command = printLoudspeakerPosition, fg='#36454f')
loudspeakerPositionButton.grid(row=13, column=4)      

###################### 13 - Calibrazione Sistema di Misura ######################

# prima della funzione creare l'input per inserire la distanza dal Loudspeaker

def measureCalWindow():
    measureCalWindow = tk.Tk()
    measureCalWindow.title("System Calibration") # titolo
    measureCalWindow.geometry('470x300') # dimensioni
    measureCalWindow.config(bg='#36454f') # colore

    comment1 = tk.Label(measureCalWindow, text='SYSTEM CALIBRATION', font='Helvetica 18 bold', bg='#36454f', fg='#f7f7f7')
    comment1.place(x=140, y=10)
    comment2 = tk.Label(measureCalWindow, text="Point the capsule of the microphone connected to the first Input Channel\nto the center of the loudspeaker connected to the first Output Channel\n---\nPlace the microphone capsule at 50cm from the center of the lodspeaker\n---\nPress CALIBRATE button\nfor the latency estimation\n---\nWait 20 seconds", bg='#36454f', fg='#f7f7f7')
    comment2.place(x=10, y=50)

    variableDistance = tk.Entry(measureCalWindow, width=5)
    variableDistance.place(x=200, y=200)
    
    def systemTare():
        global systemLatency
        buffer = np.zeros(3)
        fs = int(variableFreq.get())
        inputDevice = int(variableInputDev.get()[0])
        outputDevice = int(variableOutputDev.get()[0])

        if variableSoundSpeed.get() == 'Set default value (343 [m/s])':
            c = 343
        elif variableSoundSpeed.get() == 'Insert temperature in °C below':
            c = (331.3 + 0.606*float(t.get())) # m/s
        else:
            c = 343

        d = float(variableDistance.get())

        # by default the tare uses sine sweep since the only information neede is the pirst peak position
        for i in np.arange(0,len(buffer)):
            RIRmeasure_function(fs,1, 1, inputDevice, outputDevice, 'Tare')    
            tareRIR = np.load('SineSweepMeasures/_lastMeasureData_/RIRac.npy')
            tareRIR = tareRIR[:,0]
            firstPeak = find_directPath(tareRIR)
            sampleDist = (d/c)*fs
            buffer[i] = int(firstPeak-sampleDist)
            shutil.rmtree('SineSweepMeasures/Tare') # Delete the tare folder

        systemLatency = int(np.average(buffer))

    measureCalibrationButton = tk.Button(measureCalWindow, height=2, width=10, text="CALIBRATE",command=systemTare, font='Helvetica 16 bold', fg='#36454f')
    measureCalibrationButton.place(x=170, y=230)   

    # cancellare la cartella 'Tare'

    measureCalWindow.mainloop()

testSignalButton = tk.Button(mainWindow, height=1, width=38, text="13) CLICK HERE to calibrate the system", command=measureCalWindow, fg='#36454f')
testSignalButton.grid(row=15, column=4)   

###################### 14 - START MEASURE BUTTON ######################
def multipleStartFunctions(): # to get all the needed varaibles
    ### DEFINIZIONE VARIABILI ###
    #input/output device
    inputDevice = int(variableInputDev.get()[0])
    outputDevice = int(variableOutputDev.get()[0])
    
    #number of inputs/outputs
    inputChannels = int(variableInputCh.get())
    outputChannels = int(variableOutputCh.get())
    
    #measure name
    measureName = Name.get()
    
    #soundspeed
    if variableSoundSpeed.get() == 'Set default value (343 [m/s])':
        c = 343
    elif variableSoundSpeed.get() == 'Insert temperature in °C below':
        c = (331.3 + 0.606*float(t.get())) # m/s
    else:
        c = 343
    
    #delay type
    if variableDelay.get() == 'Delay estimation':
        delayType = 1
    elif variableDelay.get() == 'NO Delay estimation':
        delayType = 2
    
    #calibration type
    if variableCal.get() == '2D calibration':
        cal_type = 1
    elif variableCal.get() == '3D calibration':
        cal_type = 2
    
    #sampling frequency
    fs = int(variableFreq.get())
    
    #measure type
    if variableMeasure.get() == 'SineSweep':
        measureMethod = 1
    elif variableMeasure.get() == 'MLS':
        measureMethod = 2
    elif variableMeasure.get() == 'PyRoomAcoustics simulation':
        measureMethod = 3

    # print all variables on Terminal
    print('\n')
    print('Measure Name: %s' %measureName)
    print('Number of Input Channels: %d' %inputChannels)
    print('Number of Output Channels: %d' %outputChannels)
    print('Measure Type: %d' %measureMethod)
    print('Calibration Type: %d' %cal_type)
    print('Delay Estimation Type: %d' %delayType)
    print('Sampling Frequency [Hz]: %d' %fs)
    print('Sound Speed [m/s]: %.2f' %c)
    print('Room Dimensions X, Y, Z [m]: %.2f, %.2f, %.2f' %(x_axis, y_axis, z_axis))
    print('Loudspeaker known positions vector:')
    print(knownPos)
    print('\n')

    ## CREAZIONE CARTELLE ##
    #creazione cartelle misura primcipali (SineSweep & MLS)
    dirnameSineSweep = 'SineSweepMeasures/'
    dirnameMLS = 'MLSMeasures/'
    if os.path.exists(dirnameSineSweep):
        dirSineSweepFlag = True
    else :
        dirSineSweepFlag = False
    
    if os.path.exists(dirnameMLS):
        dirMLSFlag = True
    else :
        dirMLSFlag = False

    if dirSineSweepFlag == False:
        os.mkdir('SineSweepMeasures/')
        dirSineSweepFlag = True

    if dirMLSFlag == False:
        os.mkdir('MLSMeasures/')
        dirMLSFlag = True

    #creazione cartella _lastMeasureData_
    dirnameLast1 = 'SineSweepMeasures/_lastMeasureData_'
    dirnameLast2 = 'MLSMeasures/_lastMeasureData_'
    if os.path.exists(dirnameLast1):
        dirLast1Flag = True
    else :
        dirLast1Flag = False
    
    if os.path.exists(dirnameLast2):
        dirLast2Flag = True
    else :
        dirLast2Flag = False

    if dirLast1Flag == False:
        os.mkdir('SineSweepMeasures/_lastMeasureData_')
        dirLast1Flag = True

    if dirLast2Flag == False:
        os.mkdir('MLSMeasures/_lastMeasureData_')
        dirLast2Flag = True

    #creazione sottocartelle con dati misura
    if dirSineSweepFlag == True and measureMethod == 1:
        dirname1 = 'SineSweepMeasures/' + str(measureName)
        os.mkdir(dirname1)
    elif dirMLSFlag == True and measureMethod == 2:
        dirname2 = 'MLSMeasures/' + str(measureName)
        os.mkdir(dirname2)
    
    ## CREAZIONE FILE DI TESTO ##
    # SineSweep measure
    if measureMethod == 1:
        with open('SineSweepMeasures/' + str(measureName) + '/measureData.txt', 'w') as f:
         f.write('RIR MEASUREMENT DATA\n\n')
         f.write('Measure Name: %s\n' %measureName)
         f.write('Type of measure: SineSweep \nSound speed: %.2f [m/s] \nSampling Frequency: %d [Hz]\nNumber of Microphones: %d \nNumber of Loudspeakers: %d\n' %(c, fs, inputChannels, outputChannels))
         if cal_type == 1 :
             f.write('Calibration Type: 2D\n')
         elif cal_type == 2 :
             f.write('Calibration Type: 3D\n')
         if delayType == 1 :
             f.write('Delay compensation: YES\n')
         elif delayType == 2 :
             f.write('Delaycompensation: NO\n')
         f.write('\nROOM DIMENSIONS:\n')
         if cal_type == 1 :
             f.write('Room X axis dimension: %.2f [m]\nRoom Y axis dimension: %.2f [m]\n' %(x_axis, y_axis))
         if cal_type == 2 :
             f.write('Room X axis dimension: %.2f [m]\nRoom Y axis dimension: %.2f [m]\nRoom Z axis dimension: %.2f [m]\n' %(x_axis, y_axis, z_axis))
         f.write('\nLOUDSPEAKER KNOWN POSITIONS:\n')
         if cal_type == 1 :
             for i in range (0,outputChannels) : 
              f.write('Loudspeaker %d:\nX position: %.2f [m]\nY position: %.2f [m]\n\n' %(i+1, knownPos[i,0], knownPos[i,1]))
         if cal_type == 2 :
             for i in range (0,outputChannels) : 
              f.write('Loudspeaker %d:\nX position: %.2f [m]\nY position: %.2f [m]\nZ position: %.2f [m]\n\n' %(i+1, knownPos[i,0], knownPos[i,1], knownPos[i,2]))

    # MLS measure
    elif measureMethod == 2:
        with open('MLSMeasures/' + str(measureName) + '/measureData.txt', 'w') as f:
         f.write('RIR MEASUREMENT DATA\n\n')
         f.write('Measure Name: %s\n' %measureName)
         f.write('Type of measure: MLS \nSound speed: %.2f [m/s] \nSampling Frequency: %d [Hz]\nNumber of Microphones: %d \nNumber of Loudspeakers: %d\n' %(c, fs, inputChannels, outputChannels))
         if cal_type == 1 :
             f.write('Calibration Type: 2D\n')
         elif cal_type == 2 :
             f.write('Calibration Type: 3D\n')
         if delayType == 1 :
             f.write('Delay compensation: YES\n')
         elif delayType == 2 :
             f.write('Delaycompensation: NO\n')
         f.write('\nROOM DIMENSIONS:\n')
         if cal_type == 1 :
             f.write('Room X axis dimension: %.2f [m]\nRoom Y axis dimension: %.2f [m]\n' %(x_axis, y_axis))
         if cal_type == 2 :
             f.write('Room X axis dimension: %.2f [m]\nRoom Y axis dimension: %.2f [m]\nRoom Z axis dimension: %.2f [m]\n' %(x_axis, y_axis, z_axis))
         f.write('\nLOUDSPEAKER KNOWN POSITIONS:\n')
         if cal_type == 1 :
             for i in range (0,outputChannels) : 
              f.write('Loudspeaker %d:\nX position: %.2f [m]\nY position: %.2f [m]\n\n' %(i+1, knownPos[i,0], knownPos[i,1]))
         if cal_type == 2 :
             for i in range (0,outputChannels) : 
              f.write('Loudspeaker %d:\nX position: %.2f [m]\nY position: %.2f [m]\nZ position: %.2f [m]\n\n' %(i+1, knownPos[i,0], knownPos[i,1], knownPos[i,2]))      

    ## MISURA ##
    if measureMethod == 1 :
        # Misura SineSweep
        data = createDataMatrix(inputChannels,outputChannels)
        for i in np.arange(1, outputChannels+1) :
            RIRmeasure_function (fs,inputChannels, i, inputDevice, outputDevice, measureName, latency= systemLatency)
            data = fillDataMatrix(data,inputChannels,i-1)
    elif measureMethod == 2 :
        # Misura MLS
        data = createDataMatrix(inputChannels,outputChannels)
        for i in np.arange(1, outputChannels+1) :
            MLSmeasure_function (fs,inputChannels, i, inputDevice, outputDevice, measureName)
            data = fillDataMatrix(data,inputChannels,i-1)
    #elif measureMethod == 3 :
    #    data = createRir(knownPos, cal_type, delayType)

    ## CALIBRAZIONE ##
    calculate_Calibration(data, inputChannels, cal_type, delayType, measureMethod, c, fs, knownPos, x_axis, y_axis, z_axis, measureName)

buttonStart = tk.Button(mainWindow, height=2, width=30, text="14) START MEASURE", font='Helvetica 18 bold', command=multipleStartFunctions, fg='#36454f') # Inserisci command = funzione main tra text e fg per far partire misura
buttonStart.grid(row=17, column=4)

# 15 - Print Posizione Microfoni stimata ###################### -> TO DO
micPositionPrintLabel = tk.Button(mainWindow, height=2, width=30, text="15) CLICK HERE after the measure to show the\nMicrophone position estimation plot",fg='#36454f')
micPositionPrintLabel.grid(row=16, column=2)

mainWindow.mainloop()

# END