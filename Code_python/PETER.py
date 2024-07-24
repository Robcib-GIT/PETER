import os
import time
import serial
import collections
import numpy as np
from tensorflow import keras

# Get current working directory
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

# For returning the position, times, and number of iterations
MovingStats = collections.namedtuple('MvoingStats', ['pos', 'times', 'it', 'interm_pos'])

# Classe PAUL pour contrôler les valves
class PETER:
    def __init__(self, port, baudrate=115200, deflating_ratio=1.7, real_mode=True):
        self.serial_device = serial.Serial(port, baudrate, timeout=1)
        self.deflating_ratio = deflating_ratio
        self.real_mode = real_mode
        self.interm_pos = []
        # Load models
        self.pos2time = keras.models.load_model(curr_dir + 'pos2time_model.keras')
        #self.time2pos = keras.models.load_model(curr_dir + 'time2pos_model.keras')
    
    def close(self):
        self.serial_device.close()

    def write_one_valve_millis(self, valv, millis):
        if self.real_mode:
            if millis > 0:
                command = f"f,{valv},{millis}\n"  # Commande pour gonfler
            else:
                command = f"e,{valv},{-millis}\n"  # Commande pour dégonfler
            self.serial_device.write(command.encode())
            time.sleep(0.1)  # Petite pause pour s'assurer que la commande est bien envoyée

    # Fonction pour lire les données IMU
    def read_imu_data(self):
        self.serial_device.write(b'M')  # Envoyer la commande 'M' pour lire les données
        data = self.serial_device.readline().decode('utf-8').strip()  # Lire la ligne envoyée par l'Arduino

        try:
            x, y, z = map(float, data.split(","))
            return x, y, z
        except ValueError:
            print(f"Erreur de conversion des données reçues: {data}")
            return None, None, None
        
    # Callibrate the IMU
    def callibrate_imu(self):
        # Lire la position initiale
        print("Lecture de la position initiale...")
        initial_x, initial_y, initial_z = self.read_imu_data()

        if initial_x is not None and initial_y is not None and initial_z is not None:
            # Appliquer la transformation des axes sur la position initiale
            initial_x_transformed = -initial_z  # Z devient -X
            initial_y_transformed = -initial_y
            initial_z_transformed = -initial_x
            self.x0 = initial_x_transformed
            self.y0 = initial_y_transformed
            self.z0 = initial_z_transformed
            print(f"Position initiale définie à : x={initial_x_transformed}, y={initial_y_transformed}, z={initial_z_transformed}")
        else:
            print("Erreur de lecture de la position initiale. Veuillez vérifier les connexions.")
            exit()
        
    # Transformer les données IMU
    def transform_imu_data(self, x, y, z):
        new_x = -z  # Z devient -X
        new_y = -y  # Y devient -Y
        new_z = -x  # X devient -Z

        new_x = new_x - self.x0
        new_y = new_y - self.y0
        new_z = new_z - self.z0

        return new_x, new_y, new_z
    
    # Read and transform the IMU data
    def read_and_transform_imu_data(self):
        x, y, z = self.read_imu_data()
        if x is not None and y is not None and z is not None:
            return self.transform_imu_data(x, y, z)
        else:
            return None, None, None
        
    # Fonction pour gérer les opérations des valves et lire les données IMU après chaque opération
    def operate_valve_and_read_position(self, valve, duration):
        self.write_one_valve_millis(valve, duration)  # Opération sur la valve
        time.sleep(2)  # Temps d'attente après l'opération sur la valve

        # Lire les nouvelles données de position IMU
        x, y, z = self.read_imu_data()

        if x is not None and y is not None and z is not None:
            # Appliquer la transformation des axes sur les nouvelles données
            new_x = -z  # Z devient -X
            new_y = -y  # Y devient -Y
            new_z = -x  # X devient -Z

            # Calculer les positions relatives par rapport à la position initiale transformée
            relative_x = new_x - self.x0
            relative_y = new_y - self.y0
            relative_z = new_z - self.z0

            print(f"Position relative après manipulation de la valve {valve} : x={relative_x:.2f}, y={relative_y:.2f}, z={relative_z:.2f}")

            return relative_x, relative_y, relative_z
        else:
            print(f"Impossible de lire les données IMU après manipulation de la valve {valve}.")
            return None, None, None
        
    # Move to point
    def move (self, x0, y0):

        # Setting the data
        orn = np.array([[x0, y0]])
        tol = 50
        max_it = 20        

        # Calculate the time for each valve
        time0 = self.pos2time.predict(orn)[0][0]
        time1 = self.pos2time.predict(orn)[0][1]
        time2 = self.pos2time.predict(orn)[0][2]

        print(f"time0={time0:.2f}, time1={time1:.2f}, time2={time2:.2f}")

        err = [time0, time1, time2]

        it = 0
        times = [0, 0, 0]
        print(f"err0={err[0]:.2f}, err1={err[1]:.2f}, err2={err[2]:.2f}")
        #while (abs(err[0]) > tol or abs(err[1]) > tol or abs(err[2]) > tol) and it < max_it:
        while np.linalg.norm(err) > tol and it < max_it:
            it = it + 1

            print(it)

            # Correct the error
            for i in range(3):
                if err[i] > 0:
                    times[i] = min(err[i], 400)
                else:
                    times[i] = max(err[i] * self.deflating_ratio, -400)

            # Operate the valves
            for i in range(3):
                self.write_one_valve_millis(i, times[i])

            time.sleep(1)

            # Measure
            x, y, _ = self.read_and_transform_imu_data()
            self.interm_pos.append([x,y])
            time.sleep(0.5)

            # Estimate inflation times
            t0_obs = self.pos2time.predict(np.array([[x, y]]))[0][0]
            t1_obs = self.pos2time.predict(np.array([[x, y]]))[0][1]
            t2_obs = self.pos2time.predict(np.array([[x, y]]))[0][2]

            print(f"t0_obs={t0_obs:.2f}, t1_obs={t1_obs:.2f}, t2_obs={t2_obs:.2f}")

            # Calculate the error
            err[0] = time0 - t0_obs
            err[1] = time1 - t1_obs
            err[2] = time2 - t2_obs

            print(f"err0={err[0]:.2f}, err1={err[1]:.2f}, err2={err[2]:.2f}")

        x, y, _ = self.read_and_transform_imu_data()
        times = self.pos2time.predict(np.array([[x, y]]))[0]

        # Calculate the error between (x,y) and (x0,y0)
        err_pos = [0, 0]
        err_pos[0] = x0 - x
        err_pos[1] = y0 - y
        
        # Print the norm of the error
        print(f"Norm of the error: {np.linalg.norm(err_pos):.2f}")

        return MovingStats(pos = [x,y], times = times, it = it, interm_pos = self.interm_pos)
    
    # Move to point (option 2)
    def move2 (self, x0, y0):

        # Setting the data
        orn = np.array([[x0, y0]])
        tol = 1
        max_it = 20

        err = np.array([[0, 0]])

        it = 0
        while abs(err[0]) > tol and abs(err[1]) > tol and it < max_it:

            it = it + 1

            # Make predictions
            times = self.pos2time.predict(orn + err)[0]

            # Correct the error
            for i in range(3):
                if times[i] > 0:
                    times[i] = min(times[i], 400)
                else:
                    times[i] = max(times[i] * self.deflating_ratio, -400)

            # Operate the valves
            for i in range(3):
                self.write_one_valve_millis(i, times[i])

            time.sleep(1)

            # Measure
            x, y, _ = self.read_and_transform_imu_data()
            time.sleep(0.5)

            # Calculate the error
            err[0] = x0 - x
            err[1] = y0 - y

            print(f"err0={err[0]:.2f}, err1={err[1]:.2f},")

        return MovingStats(pos = [x,y], times = times, it = it)