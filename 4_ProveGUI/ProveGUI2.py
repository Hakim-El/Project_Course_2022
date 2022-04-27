from email.mime import audio
import tkinter as tk
import sounddevice as sd

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
   
# CREA MAIN WINDOW
mainWindow = tk.Tk()
mainWindow.title("Automatic RIR Measurement System") # titolo
mainWindow.geometry("900x700") # dimensioni
mainWindow.config(bg='#36454f') # colore

# Selezione Audio Device di Input
soundDevicesList = sd.query_devices()
variable = tk.StringVar(mainWindow)
variable.set('Select Input Audio Device')
opt1 = tk.OptionMenu(mainWindow, variable, *soundDevicesList)
opt1.place(x=10, y=40)

# Selezione Audio Device di Output
soundDevicesList = sd.query_devices()
variable = tk.StringVar(mainWindow)
variable.set('Select Output Audio Device')
opt2 = tk.OptionMenu(mainWindow, variable, *soundDevicesList)
opt2.place(x=10, y=10)

# Selezione numero canali Input
InputDevicesList = [1,2,3,4,5,6,7,8]
variable = tk.StringVar(mainWindow)
variable.set('Select the number of Inputs (Microphones)')
opt2 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt2.place(x=10, y=70)

# Selezione numero canali Output
InputDevicesList = [1,2,3,4,5,6,7,8]
variable = tk.StringVar(mainWindow)
variable.set('Select the number of Outputs (Loudspeakers)')
opt2 = tk.OptionMenu(mainWindow, variable, *InputDevicesList)
opt2.place(x=10, y=100)

# Istruzioni 1
istructions1 = tk.Label(mainWindow, text="ATTENTION!\nNumber of Inputs and outputs must be\ncoherent with the selected audio devices!",fg='#36454f')
istructions1.place(x=10, y=140)

# Istruzioni 2
istructions2 = tk.Label(mainWindow, text="Connect the selected number n of microphones to\n the first n input channels of the selected input device.\n\nConnect the selected number m of loudspeakers to\n the first m output channels of the selected output device.", fg='#36454f')
istructions2.place(x=10, y=200)

# Start Measure Button
#buttonStart = tk.Button(mainWindow, text="START MEASURE", command = , fg='#36454f') # Inserisci command per far partire misura
#buttonStart.place(x=545, y=500)

mainWindow.mainloop()