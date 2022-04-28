from email.mime import audio
import tkinter as tk
import sounddevice as sd
import scipy
import numpy as np
import os

## FUNZIONE CHE NON SERVE PIU'
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
########
# CREA MAIN WINDOW
mainWindow = tk.Tk()
mainWindow.title("Automatic RIR Measurement System") # titolo
mainWindow.geometry("900x700") # dimensioni
mainWindow.config(bg='#36454f') # colore

# 1 - Selezione Audio Device di Input
inputDeviceLabel = tk.Label(mainWindow, text="Select Input Audio Device",fg='#36454f')
inputDeviceLabel.place(x=10, y=400)

soundDevicesList = sd.query_devices()
variable = tk.StringVar(mainWindow)
variable.set('- input AudioDevice -')
opt1 = tk.OptionMenu(mainWindow, variable, *soundDevicesList)
opt1.place(x=10, y=40)

# 2 - Selezione Audio Device di Output
outputDeviceLabel = tk.Label(mainWindow, text="Select Output Audio Device",fg='#36454f')
outputDeviceLabel.place(x=10, y=450)

soundDevicesList = sd.query_devices()
variable = tk.StringVar(mainWindow)
variable.set('- output AudioDevice -')
opt2 = tk.OptionMenu(mainWindow, variable, *soundDevicesList)
opt2.place(x=10, y=10)

# 3 - Selezione numero canali Input
inputChannelLabel = tk.Label(mainWindow, text="Select the number of Input Channles (Microphones)",fg='#36454f')
inputChannelLabel.place(x=10, y=480)

InputDevicesList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
variable = tk.StringVar(mainWindow)
variable.set('- number of inputs -')
opt3 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt3.place(x=10, y=70)

# 4 - Selezione numero canali Output
outputChannelLabel = tk.Label(mainWindow, text="Select the number of Output Channels (Loudspeakers)",fg='#36454f')
outputChannelLabel.place(x=10, y=510)

InputDevicesList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
variable = tk.StringVar(mainWindow)
variable.set('- number of outputs -')
opt4 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt4.place(x=10, y=100)

## Istruzioni Collegamento 1
istructions1 = tk.Label(mainWindow, text="ATTENTION!\nNumber of Inputs and outputs must be\ncoherent with the selected audio devices!",fg='#36454f')
istructions1.place(x=10, y=140)
## Istruzioni Collegamento 2
istructions2 = tk.Label(mainWindow, text="Connect the selected number n of microphones to\n the first n input channels of the selected input device.\n\nConnect the selected number m of loudspeakers to\n the first m output channels of the selected output device.", fg='#36454f')
istructions2.place(x=10, y=200)

# 5 - Selezione tipo di misura
measureTypelLabel = tk.Label(mainWindow, text="Select the type of measure",fg='#36454f')
measureTypelLabel.place(x=250, y=400)

InputDevicesList = ['SineSweep', 'MLS','PyRoomAcoustics simulation']
variable = tk.StringVar(mainWindow)
variable.set('- select -')
opt5 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt5.place(x=250, y=10)

# 6 - Selezione Sampling Frequency

InputDevicesList = [44100, 48000,96000]
variable = tk.StringVar(mainWindow)
variable.set('Select the Sampling Frequency [Hz]')
opt2 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt2.place(x=250, y=40)

# Selezione tipo di calibrazione
InputDevicesList = ['2D calibration', '3D calibration']
variable = tk.StringVar(mainWindow)
variable.set('Select the type of calibration')
opt2 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt2.place(x=550, y=10)

# Delay o no Delay
InputDevicesList = ['Delay estimation', 'NO Delay estimation']
variable = tk.StringVar(mainWindow)
variable.set('Delay estimation selection')
opt2 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt2.place(x=550, y=40)

# Sound Speed estimation
InputDevicesList = ['Set default value (343 [m/s])', 'Insert temperature in °C below']
variable = tk.StringVar(mainWindow)
variable.set('Sound Speed')
opt2 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt2.place(x=550, y=70)
T = tk.Entry(mainWindow, width=5)
T.place(x=550, y=100)

# Start Measure Button
buttonStart = tk.Button(mainWindow, height=4, width=10, text="START MEASURE", fg='#36454f') # Inserisci command = funzione main tra text e fg per far partire misura
buttonStart.place(x=600, y=600)

mainWindow.mainloop()