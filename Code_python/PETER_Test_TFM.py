from PETER import PETER
import time

peter=PETER()

for i in range(6):
    peter.write_one_valve_millis(i-1,1000)
    time.sleep(2)

time.sleep(10)

for i in range(6):
    peter.write_one_valve_millis(i-1,-2000)
