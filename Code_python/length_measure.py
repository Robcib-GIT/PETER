'''
Read from serial port data from the VL53L0X sensor connected to Arduino controlling inflation times
Jorge F. García-Samartín
www.gsamartin.es
2024-10-02
'''

import tkinter as tk
import serial
import sys
import msvcrt
import os
import time
import numpy as np

import PETER

# Current file location
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

# Variable setup
t0 = time.time()
t1 = t0
t2 = t0
total_time = 0
data_all = []

# Inflation callback
def on_inflate_button_clicked():

    global t1, total_time

    valve_num = int(num_valv_entry.get())
    infl_time = int(infl_time_entry.get())

    total_time += infl_time
    
    print(f"Valve number: {valve_num}, Inflation time: {infl_time}")
    
    # Inflate the valve
    t1 = time.time()
    p.write_one_valve_millis(valve_num, infl_time)

# Deflation callback
def on_deflate_button_clicked():

    global t2, total_time

    valve_num = int(num_valv_entry.get())
    infl_time = int(infl_time_entry.get())

    total_time -= infl_time
    
    print(f"Valve number: {valve_num}, Inflation time: {infl_time}")
    
    # Deflate the valve
    t2 = time.time()
    p.write_one_valve_millis(valve_num, -3.5*infl_time)

# Robot setup
p = PETER.PETER(port='COM7', baudrate=115200, real_mode=True)

# Measuring Arduino setup
ser = serial.Serial('COM5', 9600)

# Configure the main window
root = tk.Tk()
root.title("Inverse Kinematics")

# Create input widgets for target values
num_valv_label = tk.Label(root, text="Valve number:")
num_valv_label.grid(row=0, column=0)
num_valv_entry = tk.Entry(root)
num_valv_entry.grid(row=0, column=1)

infl_time_label = tk.Label(root, text="Inflation time (ms):")
infl_time_label.grid(row=1, column=0)
infl_time_entry = tk.Entry(root)
infl_time_entry.grid(row=1, column=1)

# Buttons to inflate and deflate
inflate_button = tk.Button(root, text="Inflate", command=on_inflate_button_clicked)
inflate_button.grid(row=4, columnspan=2, pady=(10, 10))
deflate_button = tk.Button(root, text="Deflate", command=on_deflate_button_clicked)
deflate_button.grid(row=5, columnspan=2, pady=(10, 10))

# Run the graphical interface
while True:

    if msvcrt.kbhit() and msvcrt.getch() == b'q':
        print("Stopping data read.")
        break

    # Read from serial port data from the VL53L0X sensor connected to Arduino
    data = ser.readline()
    t = time.time()
    print(data.decode('utf-8'))

    # Get from data only the distance (remove the final \r\n)
    data = data[:-2]

    # Save all the data to an array
    data_all.append([t-t0, t-t1, t-t2, total_time, data.decode('utf-8')])

    # For the interface
    root.update_idletasks()
    root.update()

# Save data to a file named YYYY-MM-DD_HH-MM-SS_length-time.csv
t = time.localtime()
file_name = f"{t.tm_year}-{t.tm_mon}-{t.tm_mday}_{t.tm_hour}-{t.tm_min}-{t.tm_sec}_length-time.csv"
np.savetxt(curr_dir + 'results/length-time/' + file_name, np.array(data_all, dtype=object), delimiter=";", fmt='%s')