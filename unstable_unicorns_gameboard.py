import tkinter as tk
from tkinter import ttk

def convert():
    print(entry_int.get())

#window
window = tk.Tk()
window.title('Unstable Unicorns!')
window.geometry('1920x1080')

#title
title_label = ttk.Label(master=window, text = 'Miles to kilometers', font = 'Calibri 24 bold')
title_label.pack()

#input field
input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
entry = ttk.Entry(master = input_frame, textvariable = entry_int)
button = ttk.Button(master = input_frame, text = 'Convert', command = convert)
button = ttk.Button(master = input_frame, text = 'Convert', command = convert)
entry.pack(side = 'left')
button.pack(side = 'left')
button.pack(side = 'right')
input_frame.pack()

#output
output_string = tk.StringVar()
output_label = ttk.Label(master = window, text ='Output', font = 'Calibri 24')
output_label.pack(pady = 5)
#run
window.mainloop()