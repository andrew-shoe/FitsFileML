import matplotlib
import numpy as np
from astropy.io import fits
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from fitsfilemodel import SingleLabelModel
import sys


"""Kind of haggard, just for Mulan right now"""

# Tkinter has different package name on differnt python versions >:(
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog
else:
    import tkinter as tk
    import tkinter.filedialog as tkFileDialog


def load_fitsfiles(model):
    """Function that is to intialize project. Sets up the model and plots the first file"""

    x = tkFileDialog.askdirectory()
    model.set_working_dir(x)
    on_file = model.get_next_unlabeled()
    if not on_file:
        model.cur_msg.set("No unlabeled files")
        return
    else:
        plot(on_file)

def disp_next(model):
    """Displays next unlabeled fits file"""

    if not model.cur_dir:
        model.cur_msg.set("Choose a project")
        return

    on_file = model.get_next_unlabeled()

    if not on_file:
        print("No more files")
    else:
        plot(on_file)

def label(model, lbl):

    """Writes label of current displayed file to a csv"""

    if not model.working_dir:
        model.cur_msg.set("Choose a project")
    else:
        on_file = model.get_next_unlabeled() #  The current file that is displayed
        if not on_file:
            model.cur_msg.set("No more unlabeled files")
        else:
            model.write_row(on_file, lbl)
            disp_next(model)
            model.cur_msg.set("{} files left".format(len(model.get_unlabeled_files())))

def undo(model):
    """Undos previous label"""
    on_file, off_file = model.undo()
    if not on_file:
        model.cur_msg.set("Cannot undo")
        return
    else:
        plot(on_file)
        model.cur_msg.set("{} files left".format(len(model.get_unlabeled_pairs())))

def plot(file):
    """Plots given file"""
    on_plot.cla()
    on_log_plot.cla()
    on_data = fits.getdata(file)
    c_freq.set("Center Frequency: {}".format(fits.open(file)[0].header["FCNTR"]))
    on_plot.imshow(on_data, aspect=5)

    on_data_log = 10*np.log10(on_data)
    on_log_plot.imshow(on_data_log, aspect=5)
    f.suptitle(file)
    f.canvas.draw()

model = SingleLabelModel()  # Initialize model. The model controls the logic between the actual fitsfile, GUI and csv

# Everything below this is to set up GUI
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


"""The following is super haggard and should be optimized
Can easily be customized for different labels. Can even add or remove labels to your liking"""


freq_label = tk.Label(root, text="NARROW BAND")
freq_label.grid(row=2, column=1, columnspan=1)
button0 = tk.Button(root, text="[1] Diagonal (1)", padx=50, command=lambda: label(model, 0))
button0.grid(row=3, column=0)
button1 = tk.Button(root, text="[2] Diagonal (1+)", padx=50, command=lambda: label(model, 1))
button1.grid(row=3, column=1)
button2 = tk.Button(root, text="[3] Horizontal", padx=50, command=lambda: label(model, 2))
button2.grid(row=3, column=2)

button3 = tk.Button(root, text="[8] Vertical (1)", padx=50, command=lambda: label(model, 3))
button3.grid(row=4, column=0)
button4 = tk.Button(root, text="[9] Vertical (even)", padx=50, command=lambda: label(model, 4))
button4.grid(row=4, column=1)
button5 = tk.Button(root, text="[0] Vertical (inf)", padx=50, command=lambda: label(model, 5))
button5.grid(row=4, column=2)

freq_label = tk.Label(root, text="WIDE BAND")
freq_label.grid(row=5, column=1, columnspan=1)
button6 = tk.Button(root, text="[a] Diagonal (1)", padx=50, command=lambda: label(model, 6))
button6.grid(row=6, column=0)
button7 = tk.Button(root, text="[s] Diagonal (1+)", padx=50, command=lambda: label(model, 7))
button7.grid(row=6, column=1)
button8 = tk.Button(root, text="[d] Horizontal", padx=50, command=lambda: label(model, 8))
button8.grid(row=6, column=2)

button9 = tk.Button(root, text="[j] Vertical (1)", padx=50, command=lambda: label(model, 9))
button9.grid(row=7, column=0)
button10 = tk.Button(root, text="[k] Vertical (even)", padx=50, command=lambda: label(model, 10))
button10.grid(row=7, column=1)
button11 = tk.Button(root, text="[l] Vertical (inf)", padx=50, command=lambda: label(model, 11))
button11.grid(row=7, column=2)

freq_label = tk.Label(root, text="OTHER")
freq_label.grid(row=8, column=1, columnspan=1)
button12 = tk.Button(root, text="[z] No Signal", padx=50, command=lambda: label(model, 12))
button12.grid(row=9, column=0)
button13 = tk.Button(root, text="[x] Combination", padx=50, command=lambda: label(model, 13))
button13.grid(row=9, column=1)
button14 = tk.Button(root, text="[c] Signal of Interest", padx=50, command=lambda: label(model, 14))
button14.grid(row=9, column=2)

load_project_button = tk.Button(root, text="Load Project", command=lambda: load_fitsfiles(model))
load_project_button.grid(row=10, column=1)

undo_button = tk.Button(root, text="Undo", command=lambda: undo(model))
undo_button.grid(row=10, column=2)

# Set up message box
model.cur_msg = tk.StringVar()
model.cur_msg.set("Messages will be displayed here")
msg_box = tk.Label(root, textvariable=model.cur_msg)
msg_box.grid(row=12, columnspan=3)

# Bind hotkeys
root.focus_set()

root.bind("1", lambda x: label(model, 0))
root.bind("2", lambda x: label(model, 1))
root.bind("3", lambda x: label(model, 2))

root.bind("8", lambda x: label(model, 3))
root.bind("9", lambda x: label(model, 4))
root.bind("0", lambda x: label(model, 5))

root.bind("a", lambda x: label(model, 6))
root.bind("s", lambda x: label(model, 7))
root.bind("d", lambda x: label(model, 8))

root.bind("j", lambda x: label(model, 9))
root.bind("k", lambda x: label(model, 10))
root.bind("l", lambda x: label(model, 11))

root.bind("z", lambda x: label(model, 12))
root.bind("x", lambda x: label(model, 13))
root.bind("c", lambda x: label(model, 14))


# mainloop
root.mainloop()
