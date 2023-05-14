from tkinter import *

tkWindow = Tk()
tkWindow.resizable(False, False)
tkWindow.title("Tkinter Scrollbar")

text = Text(tkWindow, height=8)
text.grid(row=0, column=0, )

scroll = Scrollbar(tkWindow, orient="vertical", command=text.yview)
scroll.grid(row=0, column=1, sticky="ns")
text['yscrollcommand'] = scroll.set
tkWindow.mainloop()
