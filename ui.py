import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from tkinter import *

import subprocess

import os

def submit():
    # Get values from inputs
    file_path = file_var.get().strip()
    output_location = output_var.get().strip()
    
    try:
        max_words = int(int_input_var.get())
    except ValueError:
        messagebox.showerror("Error", "Max words must be an integer.")
        return
    
    use_ac = ac_toggle.get()  # Boolean value

    if not file_path or not output_location:
        messagebox.showerror("Error", "Please select both input file and output directory.")
        return

    # Prepare the command to run the external Python script
    command = [
        'python', 'mian.py', 
        '--input', file_path,
        '--output', output_location,
        '--words_per_line', str(max_words)
    ]
    
    # Add autocorrect flag only if enabled
    if use_ac:
        command.append('--autocorrect')

    try:
        # Run the external script
        subprocess.run(command, check=True)
        response = messagebox.askyesno("Submission", "SRT file generated succesfully. Transcript another file?")

        if response != True:
            root.quit()

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running the script: {e}")

def browse_file():
    file = filedialog.askopenfilename()
    file_var.set(file)
    
def browse_directory():
    directory = filedialog.askdirectory()
    output_var.set(directory)

# Create the main window
root = tk.Tk()
root.title("Auto Caption")


# File directory selector
file_var = tk.StringVar()
file_button = tk.Button(root, text="Select Audio or Video to Transcribe: ", command=browse_file)
file_button.grid(row=1, column=0, pady=10)
file_label = tk.Label(root, text="Selected File: ")
file_label.grid(row=2, column=0)
file_entry = tk.Entry(root, textvariable=file_var, width=40)
file_entry.grid(row=3, column=0, pady=10)

# Output directory selector

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_var = tk.StringVar(value=desktop_path)
output_button = tk.Button(root, text="Select output location: ", command=browse_directory)
output_button.grid(row=4, column=0, pady=10)
output_label = tk.Label(root, text="Selected Location: ")
output_label.grid(row=5, column=0)
output_entry = tk.Entry(root, textvariable=output_var, width=40)
output_entry.grid(row=6, column=0, pady=10)

# Frame and Grid configuration for Integer input
input_frame = Frame(root)
input_frame.grid(row=7, column=0, sticky="ew")

int_input_label = tk.Label(input_frame, text="Max words on screen at one time:")
int_input_label.pack(side=LEFT)

int_input_var = tk.StringVar(value=5)
int_input_entry = tk.Entry(input_frame, textvariable=int_input_var, width=5)
int_input_entry.pack(side=LEFT)

# Configure column weight to make the integer input and label span the full width
root.grid_columnconfigure(0, weight=1)

# Boolean selector (Checkbutton)
ac_toggle = tk.BooleanVar(value=True)
boolean_selector = tk.Checkbutton(root, text="Use Autocorrect", variable=ac_toggle)
boolean_selector.grid(row=8, column=0, pady=10)

# Submit button
submit_button = tk.Button(root, text="Start", command=submit)
submit_button.grid(row=9, column=0, pady=20)

# Onszik Inc.
sig = tk.Label(root, text="App by Onszik for GWASS6000")
sig.grid(row=10, column=0)

# Run the main loop
root.mainloop()
