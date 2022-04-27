import tkinter as tk
import tkinter.ttk as ttk
import sounddevice as sd

# REFERENCE: https://www.pythontutorial.net/tkinter/

### COSE DA METTERE
# //Selezione Device Audio Input da lista -> print query_devices + menù a tendina/casella inserimento indice/tasto
# //Selezione Device audio Output da lista -> print query_devices + menù a tendina/casella inserimento indice/tasto
# //Selezione Numero Canali Input (MIC) -> Casella con numero da inserire
# //Selezione Numero Canali Output (LOUDSPEAKER (max 8?)) -> Casella con numero da inserire/Menù a Tendina
## (implementazione Input/Otput mapping??) 
# //Scrivere all'utente come deve collegare le cose -> Casella di testo
# //Frequenza Campionamento (44100, 48000, 96000) -> menù a tendina
# //Scelta tipo Calibrazione 2D o 3D -> menù a tendina
# //Stima velocità del suono con temperatura -> Tasto per inserire la temperatura + casella inserimento
# //Misura con delay o non delay -> menù a tendina
# //Scelta metodo (Sinesweep, MLS) -> menù a tendina
# Posizione note delle n sorgenti -> celle con inserimento valori che si attivano progresivamente o che si autogenrano
# Tasto start per iniziare -> bottone
# Finestra in cui visualizzare il plot

root = tk.Tk()
devices = sd.query_devices()

# place a label on the root window

counter = 0

for i in devices:
    frame = tk.Frame(master=root)
    tk.Label(frame, text=counter).pack(side=tk.LEFT)
    tk.Label(frame, text=devices[counter]['name']).pack(side=tk.LEFT)
    tk.Label(frame, text=' - IN  :  {}'.format(devices[counter]['max_input_channels'])).pack(side=tk.LEFT)
    tk.Label(frame, text=' - OUT  :  {}'.format(devices[counter]['max_output_channels'])).pack(side=tk.LEFT)
    frame.pack()
    counter += 1 


# keep the window displaying
root.mainloop()
