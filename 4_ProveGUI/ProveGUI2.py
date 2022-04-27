import tkinter as tk
import sounddevice as sd

def printDevices():
    #print (sd.query_devices())
    deviceWindow = tk.Tk()
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
   

# Crea Finestra Principale
mainWindow = tk.Tk()
mainWindow.title("Automatic RIR Measurement System") # titolo
mainWindow.geometry("700x550") # dimensioni
mainWindow.config(bg='#36454f') # colore

button = tk.Button(mainWindow, text="Show Audio Devices", command=printDevices)
button.pack()

mainWindow.mainloop()