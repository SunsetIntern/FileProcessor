import tkinter
import tkinter.ttk
from Utils import *
from Constants import *

# Setup for initial screen
window = tkinter.Tk()
window.title(PROGRAM_TITLE)
window.geometry(SCREEN_SIZE)
window.resizable(True, True)

title_label = tkinter.Label(window, text=SCREEN_TITLE, font=BIGGEST_FONT)
title_label.pack()

notebook = tkinter.ttk.Notebook(window, width=900, height=500)
notebook.pack()

# Add Frames
frames = [tkinter.Frame(window) for i in range(len(FRAME_TITLE))]
for i in range(len(FRAME_TITLE)):
	notebook.add(frames[i], text=FRAME_TITLE[i])

# Set up screen for each frame
patentFileSettings = FileSettings('PATENT')
paperFileSettings = FileSettings('PAPER')

setup_savepath_screen(frames[0], patentFileSettings, paperFileSettings)
setup_main_screen(frames[1], "PATENT", patentFileSettings)
setup_main_screen(frames[2], "PAPER", paperFileSettings)

window.mainloop()
