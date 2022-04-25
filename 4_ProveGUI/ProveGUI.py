import tkinter as tk
import tkinter.ttk as ttk

# REFERENCE: https://www.pythontutorial.net/tkinter/

### COSE DA METTERE
# Selezione Device Audio Input da lista -> print query_devices + menù a tendina/casella inserimento indice/tasto
# Selezione Device audio Output da lista -> print query_devices + menù a tendina/casella inserimento indice/tasto
# Selezione Numero Canali Input (MIC) -> Casella con numero da inserire
# Selezione Numero Canali Output (LOUDSPEAKER (max 8?)) -> Casella con numero da inserire/Menù a Tendina
## (implementazione Input/Otput mapping??) //
## Scrivere all'utente come deve collegare le cose -> Casella di testo
# Frequenza Campionamento (44100, 48000, 96000) -> menù a tendina
# Scelta tipo Calibrazione 2D o 3D -> menù a tendina
# Stima velocità del suono con temperatura -> Tasto per inserire la temperatura + casella inserimento
# Misura con delay o non delay -> menù a tendina
# Scelta metodo (Sinesweep, MLS) -> menù a tendina
# Posizione note delle n sorgenti -> celle con inserimento valori che si attivano progresivamente o che si autogenrano
# Tasto start per iniziare -> bottone
# Finestra in cui visualizzare il plot

root = tk.Tk()

# place a label on the root window
message = tk.Label(root, text="Hello, World!")
message.pack()

# keep the window displaying
root.mainloop()
