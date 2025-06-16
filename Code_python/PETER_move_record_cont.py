"""
    Move PETER continuously and record its positions
    Jorge F. García-Samartín
    www.gsamartin.es
    2025-06-13
"""

import PETER
import time
from datetime import datetime

# Get current directory
import os
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

import SetupParams

params = SetupParams.SetupParams()

def main():

    # Setup values
    max_time = 1500  # Maximum time to record in milliseconds
    times_valves = [200, 1000, 1000] # Inflation time for each valve in milliseconds
    max_time = max(times_valves)  # Maximum time of inflation
    margin_times = [500, 2000] # Extra time of measurement before and after inflation in milliseconds
    max_time += sum(margin_times)  # Total time to record

    # Create PETER instance
    peter = PETER.PETER()

    # Time setup
    total_time = 0
    peter.interm_pos = []  # List to store intermediate positions
    data_read = False

    # Moving PETER
    t0 = time.time()
    t1 = t0
        
    # Record data continuously during one second
    while t1 - t0 < margin_times[0] / 1000.0:
        # Read sensors continuously
        while not data_read:    
            x, y, z, h = peter.read_sensors()
            if x is not None and y is not None and z is not None and h is not None:
                data_read = True

        # Print the position and store it
        t1 = time.time()
        params.print(f"Position: x={x:.2f}, y={y:.2f}, z={z:.2f}, h={h:.2f}")
        peter.interm_pos.append([t1, x, y, z, h])
        data_read = False

    # Inflate valves and record positions continuously
    params.print_debug("Inflating valves...")
    peter.write_one_valve_millis(1, times_valves[0])
    peter.write_one_valve_millis(2, times_valves[1])
    peter.write_one_valve_millis(3, times_valves[2])
    peter.interm_pos.append([t1, -1, -1, -1, -1])  # Placeholder for valve inflation time

    while int((t1 - t0) * 1000) < max_time:

        # Read data and store it
        while not data_read:    
            x, y, z, h = peter.read_sensors()
            if x is not None and y is not None and z is not None and h is not None:
                data_read = True

        # Print the position and store it
        t1 = time.time()
        params.print(f"Position: x={x:.2f}, y={y:.2f}, z={z:.2f}, h={h:.2f}")
        peter.interm_pos.append([t1, x, y, z, h])
        data_read = False

    params.print(f"Total recording time: {total_time} ms") 
    params.print("Recording complete.")

    # Deflate valves
    params.print_debug("Deflating valves...")
    peter.write_one_valve_millis(1, -3000)
    peter.write_one_valve_millis(2, -3000)
    peter.write_one_valve_millis(3, -3000)

    # Save the recorded positions
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-peter_positions.csv")
    params.print(f"Saving results to {filename}...")
    total_time = int((t1 - t0) * 1000)  # Total time in milliseconds
    with open(curr_dir + "results/dynamics/" + filename, "w") as f:
        f.write(f"Total recording time: {total_time} ms\n")
        f.write(f"Valve inflation times (ms): {times_valves}\n")
        f.write("time, x, y, z, h\n")
        for pos in peter.interm_pos:
            f.write(f"{pos[0]}, {pos[1]}, {pos[2]}, {pos[3]}, {pos[4]}\n")

if __name__ == "__main__":
    main()