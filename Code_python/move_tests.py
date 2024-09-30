import PETER
import time
import os 
import numpy as np

# Get current working directory
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

def main():

    p = PETER.PETER('COM7')

    p.callibrate_imu()

    # Generate 20 random positions between -12 and 12
    positions_references = np.random.randint(-12, 12, (5,2))
    #positions_references =[[20,0]]

    positions = []
    times = []
    iterations = []
    durations = []
    interm_pos_all = []
    k = 0

    # Move the legs to the positions
    for pos_ref in positions_references:
        print(k)
        t1 = time.time()
        pos, t, it, interm_pos = p.move(pos_ref[0],pos_ref[1])
        t2 = time.time()
        positions.append(pos)
        times.append(t)
        iterations.append(it)
        durations.append(t2-t1)
        interm_pos_all.append(interm_pos)
        k = k+1

        time.sleep(5)

    # Save the results to a csv file with the current date, hour minute and seconds
    np.savetxt(curr_dir + "results/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "_positions.csv", positions, delimiter=";")
    np.savetxt(curr_dir + "results/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "_positions_references.csv", positions_references, delimiter=";")
    np.savetxt(curr_dir + "results/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "_times.csv", times, delimiter=";")
    np.savetxt(curr_dir + "results/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "_iterations.csv", iterations, delimiter=";")
    np.savetxt(curr_dir + "results/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "_durations.csv", durations, delimiter=";")
    np.savetxt(curr_dir + "results/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "_interm_pos.csv", interm_pos, delimiter=";")

if __name__ == '__main__':
    main()