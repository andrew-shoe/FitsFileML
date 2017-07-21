import fitsio as fio
import matplotlib
import numpy as np
from astropy.io import fits
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from fitsfilemodel import SingleLabelModel
import sys


"""Kind of haggard, just for Mulan right now"""


if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog
else:
    import tkinter as tk
    import tkinter.filedialog as tkFileDialog


def load_fitsfiles(model):
    x = tkFileDialog.askdirectory()
    model.set_working_dir(x)
    on_file = model.get_next_unlabeled()
    if not on_file:
        model.cur_msg.set("No unlabeled pairs")
        return
    else:
        plot(on_file)

def disp_next_pair(model):

    if not model.cur_dir:
        model.cur_msg.set("Choose a project")
        return

    on_file, off_file = model.get_next_unlabeled()

    if not on_file:
        print("No more files")
    else:
        plot(on_file)

def label(model, lbl):
    if not model.working_dir:
        model.cur_msg.set("Choose a project")
    else:
        on_file, _ = model.get_next_unlabeled()
        if not on_file:
            model.cur_msg.set("No more unlabeled pairs")
        else:
            model.write_row(on_file, lbl)
            disp_next_pair(model)
            model.cur_msg.set("{} more pairs left".format(len(model.get_unlabeled_pairs())))

def undo(model):
    on_file, off_file = model.undo()
    if not on_file:
        model.cur_msg.set("Cannot undo")
        return
    else:
        plot(on_file)
        model.cur_msg.set("{} more pairs left".format(len(model.get_unlabeled_pairs())))

def plot(file):
    on_plot.cla()
    on_log_plot.cla()
    on_data = fio.read(file)
    c_freq.set("Center Frequency: {}".format(fits.open(file)[0].header["FCNTR"]))
    on_plot.imshow(on_data, aspect=5)

    on_data_log = 10*np.log10(on_data)
    on_log_plot.imshow(on_data_log, aspect=5)
    f.suptitle(file)
    f.canvas.draw()

model = SingleLabelModel()
root = tk.Tk()

root.geometry("800x700")
root.title = "GUI"
menu = tk.Menu(root)

# Create matplotlib plotting area
f = Figure(figsize=(8, 4), dpi=100)
on_plot = f.add_subplot(211)
on_log_plot = f.add_subplot(212, sharex=on_plot)
on_log_plot.set_title("Log")
f.tight_layout()
f.subplots_adjust(top=0.85)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().grid(row=0, columnspan=4)

# Create buttons and button labels
c_freq = tk.StringVar()
freq_label = tk.Label(root, textvar=c_freq)
freq_label.grid(row=1, column=2)


"""The following is super haggard and should be optimized"""

freq_label = tk.Label(root, text="NARROW BAND")
freq_label.grid(row=2, column=1, columnspan=2)
button0 = tk.Button(root, text="0", padx=50, command=lambda: label(model, 00))
button0.grid(row=3, column=0)
button1 = tk.Button(root, text="1", padx=50, command=lambda: label(model, 01))
button1.grid(row=3, column=1)
button2 = tk.Button(root, text="2", padx=50, command=lambda: label(model, 02))
button2.grid(row=3, column=2)
button3 = tk.Button(root, text="3", padx=50, command=lambda: label(model, 03))
button3.grid(row=3, column=3)
button4 = tk.Button(root, text="4", padx=50, command=lambda: label(model, 04))
button4.grid(row=4, column=0)
button5 = tk.Button(root, text="1", padx=50, command=lambda: label(model, 05))
button5.grid(row=4, column=1)
button6 = tk.Button(root, text="2", padx=50, command=lambda: label(model, 06))
button6.grid(row=4, column=2)
button7 = tk.Button(root, text="3", padx=50, command=lambda: label(model, 07))
button7.grid(row=4, column=3)

freq_label = tk.Label(root, text="NARROW BAND")
freq_label.grid(row=5, column=1, columnspan=2)
button10 = tk.Button(root, text="0", padx=50, command=lambda: label(model, 10))
button10.grid(row=6, column=0)
button11 = tk.Button(root, text="1", padx=50, command=lambda: label(model, 11))
button11.grid(row=6, column=1)
button12 = tk.Button(root, text="2", padx=50, command=lambda: label(model, 12))
button12.grid(row=6, column=2)
button13 = tk.Button(root, text="3", padx=50, command=lambda: label(model, 13))
button13.grid(row=6, column=3)
button14 = tk.Button(root, text="4", padx=50, command=lambda: label(model, 14))
button14.grid(row=7, column=0)
button15 = tk.Button(root, text="1", padx=50, command=lambda: label(model, 15))
button15.grid(row=7, column=1)
button16 = tk.Button(root, text="2", padx=50, command=lambda: label(model, 16))
button16.grid(row=7, column=2)
button17 = tk.Button(root, text="3", padx=50, command=lambda: label(model, 17))
button17.grid(row=7, column=3)

load_project_button = tk.Button(root, text="Load Project", command=lambda: load_fitsfiles(model))
load_project_button.grid(row=8, column=1)

undo_button = tk.Button(root, text="Undo", command=lambda: undo(model))
undo_button.grid(row=8, column=2)

# Set up message box
model.cur_msg = tk.StringVar()
model.cur_msg.set("Messages will be displayed here")
msg_box = tk.Label(root, textvariable=model.cur_msg)
msg_box.grid(row=9, columnspan=4)


# mainloop
root.mainloop()
