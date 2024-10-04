'''
Read from serial port data from the VL53L0X sensor connected to Arduino
Jorge F. García-Samartín
www.gsamartin.es
2024-09-23
'''

import serial
import msvcrt
import os

# Current file location
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

# Open serial port
ser = serial.Serial('COM5', 9600)
    
data_all = []
# Read data from serial port until a q is pressed
print("Press 'q' to stop reading data.")
while True:

    if msvcrt.kbhit() and msvcrt.getch() == b'q':
        print("Stopping data read.")
        break

    data = ser.readline()
    print(data.decode('utf-8'))

    # Get from data only the distance (remove the final \r\n)
    data = data[:-2]

    # Save all the data to an array
    data_all.append(data.decode('utf-8'))

# Save data to a file
with open(curr_dir + 'data.csv', 'w') as f:
    for item in data_all:
        f.write("%s\n" % item)