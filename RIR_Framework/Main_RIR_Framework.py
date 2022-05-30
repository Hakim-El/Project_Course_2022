# Moduli da importare per far funzionare il MAIN
import tkinter as tk
from tkinter import filedialog
import sounddevice as sd
import codecs, json
import numpy as np
import shutil
import os
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Moduli secondari da importare per far funzionare il MAIN
from _modules.SineSweep_RIRmeasure import RIRmeasure_function, createDataMatrix, fillDataMatrix
from _modules.MLS_RIRmeasure import MLSmeasure_function
from _modules.Calibration import calibrate, find_directPath

###################################################################################################
# CREAZIONE MAIN WINDOW
mainWindow = tk.Tk()
mainWindow.title("Automatic RIR Measurement System") # titolo
#mainWindow.geometry("925x490") # dimensioni
mainWindow.config(bg='#36454f') # colore

# MAIN WINDOW SPACING
borderSpace1 = tk.Label(mainWindow, text='', bg='#36454f').grid(row=1,rowspan=1)
borderSpace2 = tk.Label(mainWindow, text='', bg='#36454f').grid(column=1, columnspan=1)

verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=1, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=2, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=3, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=4, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=5, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=6, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=7, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=8, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=9, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=10, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=11, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=12, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=13, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=14, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=15, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=16, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=17, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=18, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=19, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=20, column=3)
verticalSpaces = tk.Label(mainWindow, text=' | ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=21, column=3)

verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=1, column=5)
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
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=19, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=20, column=5)
verticalSpaces = tk.Label(mainWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=21, column=5)

credits = tk.Label(mainWindow, text='Developed by: Hakim El Achak, Lorenzo Lellini, Jacopo Caucig', font=('Helvetica 11 italic'), bg='#36454f', fg='#000000')
credits.grid(row=21, column=4)

################################################################################################################################################
########## SECTION 1 ########## 
sect1 = tk.Label(mainWindow,text='1) SYSTEM SETTINGS', font='Helvetica 20 bold',bg='#36454f', fg='#f7f7f7' ).grid(row=1, column=2)

# misure ambienti in 3D
global variableCal
global cal_type
variableCal = '3D'
cal_type = 2

###################### 0 - Sistema Operativo ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=2, column=2)

InputDevicesListOS = ['macOS', 'Windows']
variableOS = tk.StringVar(mainWindow)
variableOS.set('- Select your OS -')
opt0 = tk.OptionMenu(mainWindow, variableOS, *InputDevicesListOS)
opt0.config(width=11)
opt0.grid(row=3, column=2)

###################### 1 - Selezione Audio Device di Input ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=4, column=2)
inputDeviceLabel = tk.Label(mainWindow, text="1) Select Input Audio Device",font='Helvetica 14', bg='#36454f', fg='#f7f7f7')
inputDeviceLabel.grid(row=5, column=2)

devicesDict = sd.query_devices()
devicesList = []

for i in np.arange(0,len(devicesDict)):
    name = f"{i} - {devicesDict[i]['name']} - IN: {devicesDict[i]['max_input_channels']} | OUT:  {devicesDict[i]['max_output_channels']}"
    devicesList.append(name)

variableInputDev = tk.StringVar(mainWindow)
variableInputDev.set('- input AudioDevice -')
#variableInputDev.trace('w', inputChanged)
opt1 = tk.OptionMenu(mainWindow, variableInputDev, *devicesList)
opt1.config(width=30)
opt1.grid(row=6, column=2)

###################### 2 - Selezione Audio Device di Output ######################
outputDeviceLabel = tk.Label(mainWindow, text="2) Select Output Audio Device",font='Helvetica 14', bg='#36454f', fg='#f7f7f7')
outputDeviceLabel.grid(row=7, column=2)

variableOutputDev = tk.StringVar(mainWindow)
variableOutputDev.set('- output AudioDevice -')
#variableOutputDev.trace('w', outputChanged)
opt2 = tk.OptionMenu(mainWindow, variableOutputDev, *devicesList)
opt2.config(width=30)
opt2.grid(row=8, column=2)

###################### 3 - Selezione numero canali Input/Output (Matrix) ######################
def inputWindow():
    inputMatrixWindow = tk.Toplevel(mainWindow)
    inputMatrixWindow.title("Input/Output Matrix") # titolo
    inputMatrixWindow.config(bg='#36454f') # colore

    ####################### Selezione numero canali Input ######################
    space = tk.Label(inputMatrixWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=1)
    space = tk.Label(inputMatrixWindow,  text=' ',font='Helvetica 8', bg='#36454f').grid(column=1)
    inputSelection = tk.Label(inputMatrixWindow, text='Select your Input channels:',font='Helvetica 14', bg='#36454f', fg='#f7f7f7').grid(row=2,column=2)
    space = tk.Label(inputMatrixWindow,  text=' ',font='Helvetica 8', bg='#36454f').grid(row=3)
    outputSelection = tk.Label(inputMatrixWindow, text='Select your Output channels:',font='Helvetica 14', bg='#36454f', fg='#f7f7f7').grid(row=4, column=2)

    idev = int(variableInputDev.get()[0])
    NInputs = devicesDict[idev]['max_input_channels']

    odev = int(variableOutputDev.get()[0])
    NOutputs = devicesDict[odev]['max_output_channels']

    inButtonState = np.zeros(NInputs)
    outButtonState = np.zeros(NOutputs)
    inputButton = []
    outputButton = []

    def inButtonPressed(idx):
        if inButtonState[idx] == 0:
            inButtonState[idx] = 1
            if variableOS.get() == 'macOS':
                inputButton[idx].configure(highlightbackground='green') # Activate with macOS
            elif variableOS.get() == 'Windows':
                inputButton[idx].configure(bg='green') # Activate with Windows OS
        elif inButtonState[idx] == 1:
            inButtonState[idx] = 0
            if variableOS.get() == 'macOS':
                inputButton[idx].configure(highlightbackground='white') # Activate with macOS
            elif variableOS.get() == 'Windows':
                inputButton[idx].configure(bg='white') # Activate with Windows OS
        
        global inputMap
        inputMap = np.nonzero(inButtonState)
        inputMap = inputMap[0]+1        

    def outButtonPressed(idx):
        if outButtonState[idx] == 0:
            outButtonState[idx] = 1
            if variableOS.get() == 'macOS':
                outputButton[idx].configure(highlightbackground='green') # Activate with macOS
            elif variableOS.get() == 'Windows':
                outputButton[idx].configure(bg='green') # Activate with Windows OS
        elif outButtonState[idx] == 1:
            outButtonState[idx] = 0
            if variableOS.get() == 'macOS':
                outputButton[idx].configure(highlightbackground='white') # Activate with macOS
            elif variableOS.get() == 'Windows':
                outputButton[idx].configure(bg='white') # Activate with Windows OS

        global outputMap
        outputMap = np.nonzero(outButtonState)
        outputMap = outputMap[0]+1

    #creazione input
    for j in range(0, NInputs):
        inputButton.append(tk.Button(inputMatrixWindow, width=1, height=1, text='%d' %(j+1), command= lambda j1=j: inButtonPressed(j1)))
        inputButton[j].grid(row=2, column=j+3)

    #creazione output
    for j in range(0, NOutputs):
        outputButton.append(tk.Button(inputMatrixWindow, width=1, height=1, text='%d' %(j+1), command= lambda j1=j: outButtonPressed(j1)))
        outputButton[j].grid(row=4, column=j+3)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=9, column=2)
in_outButton = tk.Button(mainWindow, width=35, text='3) Select your input/output channels',font='Helvetica 14', command = inputWindow, fg='#36454f')
in_outButton.grid(row=10, column=2)

###################### 4 - Selezione tipo di misura ######################
Horizontalspace = tk.Label(mainWindow,  text='-------------------------------------------------------------------',font='Helvetica 14 bold', bg='#36454f',fg='#f7f7f7').grid(row=11, column=2)
measureTypelLabel = tk.Label(mainWindow, text="4) Type of measure",font='Helvetica 14', bg='#36454f', fg='#f7f7f7')
measureTypelLabel.grid(row=12, column=2)

InputDevicesListMeasure = ['SineSweep', 'MLS']
variableMeasure = tk.StringVar(mainWindow)
variableMeasure.set('- select -')
opt5 = tk.OptionMenu(mainWindow, variableMeasure, *InputDevicesListMeasure)
opt5.config(width=8)
opt5.grid(row=13, column=2)

###################### 5 - Selezione Sampling Frequency ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=14, column=2)
frequencyLabel = tk.Label(mainWindow, text="5) Sampling frequency [Hz]",font='Helvetica 14', bg='#36454f', fg='#f7f7f7')
frequencyLabel.grid(row=15, column=2)

InputDevicesListFreq = [44100,48000,96000]
variableFreq = tk.StringVar(mainWindow)
variableFreq.set('- select -')
opt6 = tk.OptionMenu(mainWindow, variableFreq, *InputDevicesListFreq)
opt6.config(width=8)
opt6.grid(row=16, column=2)

###################### 6 - Sound Speed estimation ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=17, column=2)
soundSpeedLabel = tk.Label(mainWindow, text="6) Sound speed estimation",font='Helvetica 14', bg='#36454f', fg='#f7f7f7')
soundSpeedLabel.grid(row=18, column=2)

InputDevicesListSoundSpeed = ['Set default value (343 [m/s])', 'Insert temperature in °C below']
variableSoundSpeed = tk.StringVar(mainWindow)
variableSoundSpeed.set('- select -     ')
opt9 = tk.OptionMenu(mainWindow, variableSoundSpeed, *InputDevicesListSoundSpeed)
opt9.grid(row=19, column=2)
t = tk.Entry(mainWindow, width=5)
t.grid(row=20, column=2)

################################################################################################################################################
########## SECTION 2 ########## 
sect2 = tk.Label(mainWindow,text='2) CALIBRATION', font='Helvetica 20 bold',bg='#36454f', fg='#f7f7f7' ).grid(row=1, column=4)

###################### 1 - Calibrazione Sistema di Misura ######################
def measureCalWindow():
    measureCalWindow = tk.Toplevel(mainWindow)
    measureCalWindow.title("System Latency Calibration") # titolo
    #measureCalWindow.geometry('530x500') # dimensioni
    measureCalWindow.config(bg='#36454f') # colore

    space = tk.Label(measureCalWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=1)
    space = tk.Label(measureCalWindow,  text=' ',font='Helvetica 8', bg='#36454f').grid(column=1)
    instr1 = tk.Label(measureCalWindow,text='SYSTEM CALIBRATION INSTRUCTIONS', font='Helvetica 20 bold',bg='#36454f', fg='#f7f7f7' ).grid(row=2, column=2)
    space = tk.Label(measureCalWindow,text='\n', font='Helvetica 8',bg='#36454f', fg='#f7f7f7' ).grid(row=3, column=2)
    instr3 = tk.Label(measureCalWindow,text='1) Select an input and output channel from your selected Audio Device.\n(Suggestion: select input and output channels that are not used in the measure\nIf needed, activate another input and output channel from the input/output matrix.)\n\n2) Make a loop with a cable between the selected input and output.\n', font='Helvetica 14',bg='#36454f', fg='#f7f7f7' ).grid(row=4, column=2)
    space = tk.Label(measureCalWindow,text='\n', font='Helvetica 8',bg='#36454f', fg='#f7f7f7' ).grid(row=5, column=2)

    idev = int(variableInputDev.get()[0])
    NInputs = devicesDict[idev]['max_input_channels']

    odev = int(variableOutputDev.get()[0])
    NOutputs = devicesDict[odev]['max_output_channels']

    varcal_in = tk.StringVar(measureCalWindow)
    varcal_in.set('- input channel -')
    wi1 = tk.OptionMenu(measureCalWindow, varcal_in, *np.arange(1,NInputs+1))
    wi1.config(width=15)
    wi1.grid(row=6, column=2)
    space = tk.Label(measureCalWindow,text='\n', font='Helvetica 8',bg='#36454f', fg='#f7f7f7' ).grid(row=7, column=2)
    varcal_out = tk.StringVar(measureCalWindow)
    varcal_out.set('- output channel -')
    wi2 = tk.OptionMenu(measureCalWindow, varcal_out, *np.arange(1,NOutputs+1))
    wi2.config(width=15)
    wi2.grid(row=8, column=2)

    space = tk.Label(measureCalWindow,text='\n', font='Helvetica 8',bg='#36454f', fg='#f7f7f7' ).grid(row=9, column=2)
    instr6 = tk.Label(measureCalWindow,text='\n', font='Helvetica 8',bg='#36454f', fg='#f7f7f7' ).grid(row=10, column=2)
    instr5 = tk.Label(measureCalWindow, text='3) Click on "CALIBRATE" button to start the estimation of the System Latency.\nCalibration is needed again only if the user changes the input/output audio device.\n\n------\n\nAfter this step you can start the RIR measures.', font='Helvetica 14',bg='#36454f', fg='#f7f7f7' ).grid(row=11, column=2)

    def EstimLatency():
        global systemLatency
        indev = int(variableInputDev.get()[0])
        outdev = int(variableOutputDev.get()[0])
        fs = int(variableFreq.get())
        name = 'RIR_for_latency'
        
        varcalIN = [int(varcal_in.get())]
        varcalOUT = [int(varcal_out.get())]
        
        RIRmeasure_function(fs, indev, outdev, name, input_mapping= varcalIN, output_mapping= varcalOUT) 
        latencyRIR = np.load('SineSweepMeasures/_lastMeasureData_/RIR.npy')
        latencyRIR = latencyRIR.reshape((latencyRIR.shape[0],))
        systemLatency = find_directPath(latencyRIR)
        shutil.rmtree('SineSweepMeasures/RIR_for_latency') # Delete the Latency measure folder
        print('SystemLatency = %d' %systemLatency)

    space = tk.Label(measureCalWindow,text='\n', font='Helvetica 8',bg='#36454f', fg='#f7f7f7' ).grid(row=12, column=2)   
    signalTest = tk.Button(measureCalWindow, width= 8, height= 1, text='CALIBRATE', font='Helvetica 16 bold', command=EstimLatency, fg='#36454f').grid(row=13, column=2)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=2, column=4)
testSignalButton = tk.Button(mainWindow, height=1, width=35, text="1) System latency calibration", command=measureCalWindow,font='Helvetica 14', fg='#36454f')
testSignalButton.grid(row=3, column=4)   

###################### 1 - Nome della misura ######################
space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=4, column=4)
measureNameLabel = tk.Label(mainWindow, text="2) Insert the name of the measure below",font='Helvetica 14', bg='#36454f', fg='#f7f7f7')
measureNameLabel.grid(row=5, column=4)
Name = tk.Entry(mainWindow, width=34)
Name.grid(row=6, column=4)

###################### 2 - Dimensioni della stanza ######################
def printRoomDimension():
    dimension2DWindow = tk.Toplevel(mainWindow)
    dimension2DWindow.title("Room Dimensions") # titolo
    dimension2DWindow.config(bg='#36454f') # colore

    if variableCal == '2D' :
        dimension2DWindow.geometry("265x160") # dimensioni
        space = tk.Label(dimension2DWindow, height=1,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=1)
        space = tk.Label(dimension2DWindow, height=1,  text='\n',font='Helvetica 8', bg='#36454f').grid(column=1)

        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:', bg='#36454f', fg='#f7f7f7')
        xAxisLabel.grid(row=2, column=2)
        x_dim = tk.Entry(dimension2DWindow, width=5)
        x_dim.grid(row=2, column=3)

        space = tk.Label(dimension2DWindow,  text='',font='Helvetica 8', bg='#36454f').grid(row=3)
        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:', bg='#36454f', fg='#f7f7f7')
        yAxisLabel.grid(row=4, column=2)
        y_dim = tk.Entry(dimension2DWindow, width=5)
        y_dim.grid(row=4, column=3)

        z_dim = tk.StringVar(dimension2DWindow) 
        z_dim.set('0.0')

    elif variableCal == '3D':
        dimension2DWindow.geometry("265x200") # dimensioni
        space = tk.Label(dimension2DWindow, height=1,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=1)
        space = tk.Label(dimension2DWindow, height=1,  text='\n',font='Helvetica 8', bg='#36454f').grid(column=1)

        xAxisLabel = tk.Label(dimension2DWindow, text='Insert room X dimension [m]:', bg='#36454f', fg='#f7f7f7')
        xAxisLabel.grid(row=2, column=2)
        x_dim = tk.Entry(dimension2DWindow, width=5)
        x_dim.grid(row=2, column=3)

        space = tk.Label(dimension2DWindow,  text='',font='Helvetica 8', bg='#36454f').grid(row=3)
        yAxisLabel = tk.Label(dimension2DWindow, text='Insert room Y dimension [m]:', bg='#36454f', fg='#f7f7f7')
        yAxisLabel.grid(row=4, column=2)
        y_dim = tk.Entry(dimension2DWindow, width=5)
        y_dim.grid(row=4, column=3)
       
        space = tk.Label(dimension2DWindow,  text='',font='Helvetica 8', bg='#36454f').grid(row=5)
        zAxisLabel = tk.Label(dimension2DWindow, text='Insert room Z dimension [m]:', bg='#36454f', fg='#f7f7f7')
        zAxisLabel.grid(row=6, column=2)
        z_dim = tk.Entry(dimension2DWindow, width=5)
        z_dim.grid(row=6, column=3)

    def getRoomDimensions():
        global x_axis
        global y_axis
        global z_axis

        x_axis = float(x_dim.get())
        y_axis = float(y_dim.get())
        z_axis = float(z_dim.get())
    
    getDimensions = tk.Button(dimension2DWindow, text='CLICK HERE to\nconfirm dimemsions', command=getRoomDimensions, fg='#36454f')

    if variableCal == '2D' :
        space = tk.Label(dimension2DWindow,  text='',font='Helvetica 8', bg='#36454f').grid(row=5)
        getDimensions.grid(row=6, column=2)
    elif variableCal == '3D':
        space = tk.Label(dimension2DWindow,  text='',font='Helvetica 8', bg='#36454f').grid(row=7)
        getDimensions.grid(row=8, column=2)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=7, column=4)
roomDimensionButton = tk.Button(mainWindow, height=1, width=35, text="3) Insert room dimensions",font='Helvetica 14', command = printRoomDimension, fg='#36454f')
roomDimensionButton.grid(row=8, column=4)

###################### 3 - Posizione Loudspeakers ######################
def printLoudspeakerPosition():
    var_i = len(outputMap)
    LoudSpeakerWindow = tk.Toplevel(mainWindow)
    LoudSpeakerWindow.title("Insert Loudspeakers/Microphones Known Positions") # titolo
    LoudSpeakerWindow.geometry('%dx%d' %(760, (8+(var_i*100)/3))) # dimensioni
    LoudSpeakerWindow.config(bg='#36454f') # colore

    if variableCal == '2D' :
        global x_pos 
        global y_pos
        global z_pos
        x_pos = []
        y_pos = []
        z_pos = 0
        
        for i in range(var_i):
            tk.Label(LoudSpeakerWindow, text= "Known Position " + str(i+1) + " (X ; Y)",  bg='#36454f', fg='#f7f7f7').grid(row=2+i, column=1)
            x_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            x_pos[i].grid(row=2+i, column=2)
            y_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            y_pos[i].grid(row=2+i, column=3)

    elif variableCal == '3D' :
        x_pos = []
        y_pos = []
        z_pos = []
        for i in range(var_i):
            tk.Label(LoudSpeakerWindow, text= "Known Position " + str(i+1) + " (X ; Y ; Z)",  bg='#36454f', fg='#f7f7f7').grid(row=2+i, column=1)
            x_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            x_pos[i].grid(row=2+i, column=2)
            y_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            y_pos[i].grid(row=2+i, column=3)
            z_pos.append(tk.Entry(LoudSpeakerWindow, width=5))
            z_pos[i].grid(row=2+i, column=4)

    def getLoudSpeakersPositions():
        global knownPos
        if variableCal == '2D' :
            knownPos = np.zeros((var_i,2))
            for i in range(0,var_i) : 
                knownPos[i,0] = float(x_pos[i].get())
                knownPos[i,1] = float(y_pos[i].get())
        elif variableCal == '3D' :
            knownPos = np.zeros((var_i,3))
            for i in range(0,var_i) : 
                knownPos[i,0] = float(x_pos[i].get())
                knownPos[i,1] = float(y_pos[i].get())
                knownPos[i,2] = float(z_pos[i].get())
    
    verticalSpaces = tk.Label(LoudSpeakerWindow, text='  ',font='Helvetica 16 bold',  bg='#36454f', fg='#f7f7f7').grid(row=2, column=5)
    getPositions = tk.Button(LoudSpeakerWindow, text='CLICK HERE to confirm and acquire the manually entered known positions', font='Helvetica 14',command=getLoudSpeakersPositions, fg='#36454f')
    getPositions.grid(row=2, column=6)
    space = tk.Label(LoudSpeakerWindow,  text=' ',font='Helvetica 8', bg='#36454f').grid(row=3, column=6)
    Horizontalspace = tk.Label(LoudSpeakerWindow,  text='-----------------------------------------------------------------------------------------------------------',font='Helvetica 14 bold', bg='#36454f',fg='#f7f7f7').grid(row=4, column=6)
    
################## Load knownPos from external json #########
def loadWindow():
    loadJSON = tk.Toplevel(mainWindow)
    loadJSON.title("Import Loudspeakers/Microphones Known Positions") # titolo
    #loadJSON.geometry('400' %(890, (250+(var_i*100)/3))) # dimensioni
    loadJSON.config(bg='#36454f') # colore

    def loadJson():
        measureName = Name.get()
        if variableMeasure.get() == 'SineSweep':
            with open('SineSweepMeasures/' + str(measureName) + '/measureData.json', 'r') as openfile:
                json_object = json.load(openfile)
        elif variableMeasure.get() == 'MLS':
            with open('MLSMeasures/' + str(measureName) + '/measureData.json', 'r') as openfile:
                json_object = json.load(openfile)
        global knownPos
        knownPos = np.asarray(json_object['Estimated positions'])

    space = tk.Label(loadJSON,  text=' ',font='Helvetica 8', bg='#36454f').grid(row=1)
    space = tk.Label(loadJSON,  text=' ',font='Helvetica 8', bg='#36454f').grid(column=1)
    space = tk.Label(loadJSON,  text=' ',font='Helvetica 8', bg='#36454f').grid(row=2, column=1)
    measure = tk.Label(loadJSON, text="1) Enter the name of an existing measure from which you want to import data:", font='Helvetica 14',bg='#36454f', fg='#f7f7f7').grid(row=3, column=1)
    prevuiousMeasure = tk.Entry(loadJSON, width=21)
    prevuiousMeasure.grid(row=4, column=1)
    measureType = tk.Label(loadJSON, text="2) Enter the type of the existing measure from which you want to import data:",font='Helvetica 14',bg='#36454f', fg='#f7f7f7').grid(row=5, column=1)
    InputDevicesListPREV = ['SineSweep', 'MLS']
    variablePREV = tk.StringVar(loadJSON)
    variablePREV.set('- Select -')
    optPREV = tk.OptionMenu(loadJSON, variablePREV, *InputDevicesListPREV)
    optPREV.config(width=17)
    optPREV.grid(row=6, column=1)
    
    loadFile = tk.Label(loadJSON, text="3) Enter the type of data of the existing measure:",font='Helvetica 14',bg='#36454f', fg='#f7f7f7').grid(row=7, column=1)
    InputDevicesListDATA = ['Positions from a calibration', 'Known positions']
    variableDATA = tk.StringVar(loadJSON)
    variableDATA.set('- Select -')
    optDATA = tk.OptionMenu(loadJSON, variableDATA, *InputDevicesListDATA)
    optDATA.config(width=17)
    optDATA.grid(row=8, column=1)

    space = tk.Label(loadJSON,  text=' ',font='Helvetica 8', bg='#36454f').grid(row=9, column=1)
    loadPositions = tk.Button(loadJSON, text='4) CLICK HERE to load positions from an existing json file',font='Helvetica 14',command=loadJson, fg='#36454f').grid(row=10, column=1)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=9, column=4)
loudspeakerPositionButton = tk.Button(mainWindow,width= 35, text="4a) Insert known positions manually",font='Helvetica 14', command = printLoudspeakerPosition, fg='#36454f')
loudspeakerPositionButton.grid(row=10, column=4) 

loudspeakerPositionButton = tk.Button(mainWindow,width= 35, text="4b) Import known positions from a json file",font='Helvetica 14', command = loadWindow, fg='#36454f')
loudspeakerPositionButton.grid(row=11, column=4)     

###################### 4 - START MEASURE BUTTON ######################
def multipleStartFunctions(): # to get all the needed varaibles
    ### DEFINIZIONE VARIABILI ###
    #input/output device
    inputDevice = int(variableInputDev.get()[0])
    outputDevice = int(variableOutputDev.get()[0])
    
    #number of inputs/outputs
    inputChannels = len(inputMap)
    outputChannels = len(outputMap)
    
    #measure name
    measureName = Name.get()
    
    #soundspeed
    if variableSoundSpeed.get() == 'Set default value (343 [m/s])':
        c = 343
    elif variableSoundSpeed.get() == 'Insert temperature in °C below':
        c = (331.3 + 0.606*float(t.get())) # m/s
    else:
        c = 343

    #calibration type
    if variableCal == '2D':
        cal_type = 1
    elif variableCal == '3D':
        cal_type = 2
    
    #sampling frequency
    fs = int(variableFreq.get())
    
    #measure type
    if variableMeasure.get() == 'SineSweep':
        measureMethod = 1
    elif variableMeasure.get() == 'MLS':
        measureMethod = 2

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

    ## MISURA ##
    if measureMethod == 1 :
        # Misura SineSweep
        RIRmeasure_function (fs, inputDevice, outputDevice, measureName, input_mapping=inputMap, output_mapping=outputMap[0], latency= systemLatency)
        data = createDataMatrix(len(inputMap),len(outputMap))
        data = fillDataMatrix(data,len(inputMap), 1)

        outputMapNEW = outputMap[1:]
        counter = 2

        for i in outputMapNEW:
            RIRmeasure_function (fs, inputDevice, outputDevice, measureName, input_mapping=inputMap, output_mapping=i, latency= systemLatency)
            data = fillDataMatrix(data,len(inputMap),counter)
            counter =+ 1

        # save the Matrix containing ALL RIRS
        dirname = 'SineSweepMeasures/' + str(measureName)
        np.save(dirname + '/RIRMatrix.npy',data)

    elif measureMethod == 2 :
        # Misura MLS
        data = createDataMatrix(inputChannels,outputChannels)
        for i in np.arange(1, outputChannels+1) :
            MLSmeasure_function (fs,inputChannels, i, inputDevice, outputDevice, measureName, latency= systemLatency)
            data = fillDataMatrix(data,inputChannels,i-1)

    ## CALIBRAZIONE ##
    posType = 's'
    maxBuffer = 1e-3
    interpFactor = 2
    posbounds = [[0,x_axis],[0,y_axis],[0,z_axis]]
    estimatedPosition, estimatedBuffer = calibrate(data, fs, measureName, measureMethod, posType, knownPos,maxBuffer,posbounds,interpFactor,sound_speed=c,estimate_buffer=False)

    ## CREAZIONE FILE DI TESTO ##
    # SineSweep measure
    if measureMethod == 1:
        RIR_Data ={
            'Measure Name' : measureName,
            'Type of measure': 'SineSweep',
            'Sound speed': c,
            'Sampling frequency': fs,
            'Number of Microphones': inputChannels,
            'Number of Loudspeakers': outputChannels,
            'Room dimension': [x_axis, y_axis, z_axis],
            'Known positions': knownPos.tolist(),
            'Estimated positions': estimatedPosition.tolist()
        }
        json_object = json.dumps(RIR_Data, indent = 4)
        with open('SineSweepMeasures/' + str(measureName) + '/measureData.json', 'w') as outfile:
            outfile.write(json_object)

    elif measureMethod ==2:
        RIR_Data ={
            'Measure Name' : measureName,
            'Type of measure': 'MLS',
            'Sound speed': c,
            'Sampling frequency': fs,
            'Number of Microphones': inputChannels,
            'Number of Loudspeakers': outputChannels,
            'Room dimension': [x_axis, y_axis, z_axis],
            'Known positions': knownPos.tolist(),
            'Estimated positions': estimatedPosition.tolist()
        }
        json_object = json.dumps(RIR_Data, indent = 4)
        with open('MLSMeasures/' + str(measureName) + '/measureData.json', 'w') as outfile:
            outfile.write(json_object)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=12, column=4)
buttonStart = tk.Button(mainWindow, height=1, width=31, text="5) START CALIBRATION MEASURE", font='Helvetica 15 bold', command=multipleStartFunctions, fg='#36454f') # Inserisci command = funzione main tra text e fg per far partire misura
buttonStart.grid(row=13, column=4)

###################### 5 - Print Calibrazione stimata ######################
def showPlot ():
    plotWindow = tk.Toplevel(mainWindow)
    plotWindow.title("Position Estimation") # titolo
    #plotWindow.geometry('530x500') # dimensioni
    plotWindow.config(bg='#36454f') # colore
    
    #measure name
    measureName = Name.get()

    if variableMeasure.get() == 'SineSweep':
        img = ImageTk.PhotoImage(Image.open("SineSweepMeasures/"+ str(measureName) +"/CalibrationGraph.png"))
        plotLabel = tk.Label(plotWindow, image= img)
        plotLabel.grid(row=1, column=1)
    elif variableMeasure.get() == 'MLS':
        img = ImageTk.PhotoImage(Image.open("MLSMeasures/"+ str(measureName) +"/CalibrationGraph.png"))
        plotLabel = tk.Label(plotWindow, image= img)
        plotLabel.grid(row=1, column=1)

    plotWindow.mainloop()

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=14, column=4)
micPositionPrintLabel = tk.Button(mainWindow, height=1, width=35, text="6) Show Calibration plot",font='Helvetica 14', command= showPlot, fg='#36454f')
micPositionPrintLabel.grid(row=15, column=4)

###################### 6 - Print RIR ottenute ######################
def showRIR():
    RIRplot = tk.Toplevel(mainWindow)
    RIRplot.title("Room Impulse Response plot") # titolo
    #plotWindow.geometry('530x500') # dimensioni
    RIRplot.config(bg='#36454f') # colore
    
    space = tk.Label(RIRplot,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=1)
    space = tk.Label(RIRplot,  text=' ',font='Helvetica 8', bg='#36454f').grid(column=1)
    text1 = tk.Label(RIRplot, text='Select a Loudspeaker (Output channel)', font='Helvetica 14', bg='#36454f', fg='#f7f7f7').grid(row=2, column=2)
    variableRIRout = tk.StringVar(RIRplot)
    variableRIRout.set('- Loudspeaker Number -')
    optRIRout = tk.OptionMenu(RIRplot, variableRIRout, *outputMap)
    optRIRout.config(width=15)
    optRIRout.grid(row=3, column=2)
    space = tk.Label(RIRplot,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=4, column=2)
    text2 = tk.Label(RIRplot, text='Select a Microphone (Input channel)', font='Helvetica 14', bg='#36454f', fg='#f7f7f7').grid(row=5, column=2)
    variableRIRin = tk.StringVar(RIRplot)
    variableRIRin.set('- Microphone Number -')
    optRIRin = tk.OptionMenu(RIRplot, variableRIRin, *inputMap)
    optRIRin.config(width=15)
    optRIRin.grid(row=6, column=2)

    def RIRplotshow():
        RIRplot = tk.Toplevel(mainWindow)
        RIRplot.title("PLOT") # titolo
        #plotWindow.geometry('530x500') # dimensioni
        RIRplot.config(bg='#36454f') # colore

        measureName = Name.get()
        output_select = int(variableRIRout.get()) 
        input_select = int(variableRIRin.get())

        if variableMeasure.get() == 'SineSweep':
            plotRIR = np.load('SineSweepMeasures/' + str(measureName) + '/RIRMatrix.npy')
        elif variableMeasure.get() == 'MLS':
            plotRIR = np.load('MLSMeasures/' + str(measureName) + '/RIRMatrix.npy')

        inputIdx = np.where(inputMap == input_select)[0][0]
        outputIdx = np.where(outputMap == output_select)[0][0]

        figRIR = Figure(figsize=(4,4),dpi=100)
        plot1 = figRIR.add_subplot(111)
        plot1.plot(plotRIR[:,inputIdx,outputIdx])
        canvas = FigureCanvasTkAgg(figRIR, RIRplot)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,RIRplot)
        toolbar.update()
        canvas.get_tk_widget().pack()
    
    space = tk.Label(RIRplot,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=7, column=2)
    showplotbutton = tk.Button(RIRplot, height=1, width=6, text='SHOW RIR', font='Helvetica 16 bold', command=RIRplotshow).grid(row=8, column=2)

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=16, column=4)
RIRPrintLabel = tk.Button(mainWindow, height=1, width=35, text="7) Show RIRs plot",font='Helvetica 14', command= showRIR, fg='#36454f')
RIRPrintLabel.grid(row=17, column=4)

############ 1 - show estimated position ############
def printMicPositions():
    micpositionsplot = tk.Toplevel(mainWindow)
    micpositionsplot.title("Estimated Positions") # titolo
    #plotWindow.geometry('530x500') # dimensioni
    micpositionsplot.config(bg='#36454f') # colore
    
    space = tk.Label(micpositionsplot, height=1,  text='n',font='Helvetica 8', bg='#36454f').grid(row=1)
    space = tk.Label(micpositionsplot, height=1,  text='\n',font='Helvetica 8', bg='#36454f').grid(column=1)
    src1 = tk.Label(micpositionsplot, height=1,  text='Source estimated position:',font='Helvetica 14', bg='#36454f', fg='#f7f7f7').grid(row=1)
    space = tk.Label(micpositionsplot, height=1,  text='\n',font='Helvetica 8', bg='#36454f').grid(column=1)

    measureName = Name.get()
    if variableMeasure.get() == 'SineSweep':
        with open('SineSweepMeasures/' + str(measureName) + '/measureData.json', 'r') as openfile:
            estimPos = json.load(openfile)
    elif variableMeasure.get() == 'MLS':
        with open('MLSMeasures/' + str(measureName) + '/measureData.json', 'r') as openfile:
            estimPos = json.load(openfile)

    posMatrix = np.asarray(estimPos['Estimated positions'])
    
    for i in np.arange(0,posMatrix.shape[0]):
        posList = tk.Label(micpositionsplot, height=1, text= 'Pos{}: x = {} [m] ; y = {} [m] ; z = {} [m]'.format(i+1,posMatrix[i,0],posMatrix[i,1],posMatrix[i,2]), font='Helvetica 14', bg='#36454f', fg='#f7f7f7').grid(row=3+i)  

space = tk.Label(mainWindow,  text='\n',font='Helvetica 8', bg='#36454f').grid(row=18, column=4)
micPositionsLabel = tk.Button(mainWindow, height=1, width=35, text="8) Show calibration positions",font='Helvetica 14', command= printMicPositions, fg='#36454f')
micPositionsLabel.grid(row=19, column=4)

mainWindow.mainloop()
# END