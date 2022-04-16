import tkinter as tk

# REFERENCE: https://www.pythontutorial.net/tkinter/

root = tk.Tk()

# place a label on the root window
message = tk.Label(root, text="Hello, World!")
message.pack()

# keep the window displaying
root.mainloop()