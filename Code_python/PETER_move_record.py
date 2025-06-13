"""
    Move PETER and record its positions
    Jorge F. García-Samartín
    www.gsamartin.es
    2025-06-10
"""

import PETER
import time
from datetime import datetime

# Get current directory
import os
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def main():

    # Setup values
    step_time = 100  # Time between steps in milliseconds

    # Create PETER instance
    peter = PETER.PETER(port="COM7")

    # Get current time
    t0 = 0
    t1 = time.time()

    # Initialize the total time
    total_time = 0
    max_time = 1500  # Maximum time to record in milliseconds
    peter.interm_pos = []  # List to store intermediate positions
    data_read = False

    while True:
        t1 = time.time()
        print(t1 - t0)
        if t1 - t0 > step_time / 1000.0:  # Convert milliseconds to seconds

            # Sedning commands to move the valves
            peter.write_one_valve_millis(1, step_time)
            peter.write_one_valve_millis(2, step_time) 
            peter.write_one_valve_millis(3, step_time)

            # Assuming read_sensors() returns x, y, z, h
            while not data_read:    
                x, y, z, h = peter.read_sensors()
                if x is not None and y is not None and z is not None and h is not None:
                    data_read = True

            # Print the position and store it
            print(f"Position: x={x:.2f}, y={y:.2f}, z={z:.2f}, h={h:.2f}")
            peter.interm_pos.append([time.time(),x, y, z, h])
            t0 = t1
            total_time += step_time
            data_read = False
            
        # Optionally, break after some condition or run indefinitely
        if total_time >= max_time: 
            print("Recording complete.")
            break

    # Save the recorded positions
    filename = datetime.now().strftime("%Y-%m-%d-peter_positions.csv")
    with open(curr_dir + "results/" + filename, "w") as f:
        f.write(f"Total recording time: {total_time} ms\n")
        f.write(f"Step time: {step_time} ms\n")
        f.write("time, x, y, z, h\n")
        for pos in peter.interm_pos:
            f.write(f"{pos[0]}, {pos[1]}, {pos[2]}, {pos[3]}, {pos[4]}\n")

if __name__ == "__main__":
    main()