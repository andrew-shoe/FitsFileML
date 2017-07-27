import matplotlib
import numpy as np
from astropy.io import fits
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from fitsfilemodel import PairLabelModel
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog
else:
    import tkinter as tk
    import tkinter.filedialog as tkFileDialog


# Author: Andrew Xu
# Date: 7/17/17

def load_fitsfiles(model):
    """Function that is to intialize project. Sets up the model and plots the pair"""

    x = tkFileDialog.askdirectory()
    model.set_working_dir(x)
    on_file, off_file = model.get_next_unlabeled()
    if not on_file:
        model.cur_msg.set("No unlabeled pairs")
        return
    else:
        plot(on_file, off_file)

def disp_next_pair(model):
    """Displays next unlabeled pair"""

    if not model.cur_dir:
        model.cur_msg.set("Choose a project")
        return

    on_file, off_file = model.get_next_unlabeled()

    if not on_file:
        print("No more files")
    else:
        plot(on_file, off_file)

def label(model, lbl):
    """Labels pairs"""
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
    """Undos the previously labeled file"""

    on_file, off_file = model.undo()
    if not on_file:
        model.cur_msg.set("Cannot undo")
        return
    else:
        plot(on_file, off_file)
        model.cur_msg.set("{} more pairs left".format(len(model.get_unlabeled_pairs())))

def plot(on_file, off_file):
    """Plots a pair"""

    on_plot.cla()
    off_plot.cla()
    on_log_plot.cla()
    off_log_plot.cla()
    on_data = fits.getdata(on_file)
    off_data = fits.getdata(off_file)
    c_freq.set("Center Frequency: {}".format(fits.open(on_file)[0].header["FCNTR"]))
    vmin = min([np.min(on_data), np.min(off_data)])
    vmax = max([np.max(on_data), np.max(off_data)])
    on_plot.imshow(on_data, vmin=vmin, vmax=vmax, aspect=5)
    off_plot.imshow(off_data, vmin=vmin, vmax=vmax, aspect=5)

    on_data_log = 10*np.log10(on_data)
    off_data_log = 10*np.log10(off_data)
    vmin = min([np.min(on_data_log), np.min(off_data_log)])
    vmax = max([np.max(on_data_log), np.max(off_data_log)])
    on_log_plot.imshow(on_data_log, vmin=vmin, vmax=vmax, aspect=5)
    off_log_plot.imshow(off_data_log, vmin=vmin, vmax=vmax, aspect=5)
    f.suptitle(on_file)
    f.canvas.draw()

    
model = LabelModel()
root = tk.Tk()

root.geometry("800x800")
root.title = "GUI"
menu = tk.Menu(root)

# Create matplotlib plotting area
f = Figure(figsize=(8, 6), dpi=100)
on_plot = f.add_subplot(411)
on_plot.set_title("ON")
off_plot = f.add_subplot(412, sharex=on_plot)
off_plot.set_title("OFF")
on_log_plot = f.add_subplot(413, sharex=on_plot)
on_log_plot.set_title("Log ON")
off_log_plot = f.add_subplot(414, sharex=on_plot)
off_log_plot.set_title("Log OFF")
f.tight_layout()
f.subplots_adjust(top=0.85)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().grid(row=0, columnspan=5)

# Create buttons and button labels
c_freq = tk.StringVar()
freq_label = tk.Label(root, textvar=c_freq)
freq_label.grid(row=1, column=2)
label0 = tk.Label(text="Definitely RFI")
label0.grid(row=2, column=0)
label2 = tk.Label(root, text="Unsure")
label2.grid(row=2, column=2)
label3 = tk.Label(text="Definitely SoI")
label3.grid(row=2, column=4)

button0 = tk.Button(root, text="0", padx=50, command=lambda: label(model, 0))
button0.grid(row=3, column=0)
button1 = tk.Button(root, text="1", padx=50, command=lambda: label(model, 1))
button1.grid(row=3, column=1)
button2 = tk.Button(root, text="2", padx=50, command=lambda: label(model, 2))
button2.grid(row=3, column=2)
button3 = tk.Button(root, text="3", padx=50, command=lambda: label(model, 3))
button3.grid(row=3, column=3)
button4 = tk.Button(root, text="4", padx=50, command=lambda: label(model, 4))
button4.grid(row=3, column=4)

load_project_button = tk.Button(root, text="Load Project", command=lambda: load_fitsfiles(model))
load_project_button.grid(row=4, column=1)

undo_button = tk.Button(root, text="Undo", command=lambda: undo(model))
undo_button.grid(row=4, column=3)

# Set up message box
model.cur_msg = tk.StringVar()
model.cur_msg.set("Messages will be displayed here")
msg_box = tk.Label(root, textvariable=model.cur_msg)
msg_box.grid(row=5, columnspan=5)

# Bind hotkeys
root.focus_set()
root.bind("0", lambda x: label(model, 0))
root.bind("1", lambda x: label(model, 1))
root.bind("2", lambda x: label(model, 2))
root.bind("3", lambda x: label(model, 3))
root.bind("4", lambda x: label(model, 4))

# mainloop
root.mainloop()
