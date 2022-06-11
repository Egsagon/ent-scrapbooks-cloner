import tkinter as tk
from tkinter import ttk

app = tk.Tk()
app.geometry('200x200')

bar = ttk.Progressbar(app)
add = tk.Button(app, text = 'add',
                command = lambda *_: bar.step(10))

bar.pack()
add.pack()
app.mainloop()