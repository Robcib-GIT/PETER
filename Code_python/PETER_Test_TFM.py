from PETER import PETER
import time

peter=PETER("COM6")

#times = [372, 984, 202, 561, 612, 475]
#times = [194, 104, 1068, 356, 258, 459]
#times = [275, 880, 1518, 798, 970, 1016]
#times = [523, 457, 83, 266, 235, 110]
#times = [311, 1884, 162, 767, 923, 483] # Se sacan fotazas de aquí
#times = [474, 1072, 242, 500, 579, 444]
#times = [261, 101, 1173, 315, 269, 430]

#times = [282, 940, 1611, 786, 948, 1094]
#times = [672, 560, 66, 271, 0, 183]
times = [328, 1995, 47, 649, 1107, 449]

for i in range(6):
    if i != 4:
        j = i
    else:
        j = 8
    peter.write_one_valve_millis(j,times[i])
    time.sleep(2)

time.sleep(0.5)

for i in range(9):
    peter.write_one_valve_millis(i,-5000)
