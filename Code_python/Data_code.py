import serial
import time
import csv
import random

# Classe PAUL pour contrôler les valves
class PAUL:
    def __init__(self, port, baudrate=115200, deflating_ratio=5, real_mode=True):
        self.serial_device = serial.Serial(port, baudrate, timeout=1)
        self.deflating_ratio = deflating_ratio
        self.real_mode = real_mode

    def write_one_valve_millis(self, valv, millis):
        if self.real_mode:
            if millis > 0:
                command = f"f,{valv},{millis}\n"  # Commande pour gonfler
            else:
                command = f"e,{valv},{-millis}\n"  # Commande pour dégonfler
            self.serial_device.write(command.encode())
            time.sleep(0.1)  # Petite pause pour s'assurer que la commande est bien envoyée
    
    def close(self):
        self.serial_device.close()

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

# Configuration du port série pour l'IMU et PAUL
port = '/dev/ttyUSB0'
baudrate = 115200
paul = PAUL(port=port, deflating_ratio=5)

# Connexion au port série pour l'IMU
time.sleep(2)  # Attendre que la connexion série se stabilise

# Fonction pour gérer les opérations des valves et lire les données IMU après chaque opération
def operate_valve_and_read_position(valve, duration):
    paul.write_one_valve_millis(valve, duration)  # Opération sur la valve
    time.sleep(2)  # Temps d'attente après l'opération sur la valve

    # Lire les nouvelles données de position IMU
    x, y, z = paul.read_imu_data()

    if x is not None and y is not None and z is not None:
        # Appliquer la transformation des axes sur les nouvelles données
        new_x = -z  # Z devient -X
        new_y = -y  # Y devient -Y
        new_z = -x  # X devient -Z

        # Calculer les positions relatives par rapport à la position initiale transformée
        relative_x = new_x - initial_x_transformed
        relative_y = new_y - initial_y_transformed
        relative_z = new_z - initial_z_transformed

        print(f"Position relative après manipulation de la valve {valve} : x={relative_x:.2f}, y={relative_y:.2f}, z={relative_z:.2f}")

        return relative_x, relative_y, relative_z
    else:
        print(f"Impossible de lire les données IMU après manipulation de la valve {valve}.")
        return None, None, None
    
# Calibration
#print("Calibration")
#paul.write_one_valve_millis(0,2000)
#time.sleep(5)
#paul.write_one_valve_millis(1,2000)
#time.sleep(5)
#paul.write_one_valve_millis(2,2000)
#time.sleep(2)
#paul.write_one_valve_millis(0,-10000)
#paul.write_one_valve_millis(1,-10000)
#paul.write_one_valve_millis(2,-10000)
#time.sleep(10)

# Lire la position initiale
print("Lecture de la position initiale...")
initial_x, initial_y, initial_z = paul.read_imu_data()

if initial_x is not None and initial_y is not None and initial_z is not None:
    # Appliquer la transformation des axes sur la position initiale
    initial_x_transformed = -initial_z  # Z devient -X
    initial_y_transformed = -initial_y  # Y devient -Y
    initial_z_transformed = -initial_x  # X devient -Z
    
    initial_position_coords = (initial_x_transformed, initial_y_transformed, initial_z_transformed)
    print(f"Position initiale définie à : x={initial_x_transformed}, y={initial_y_transformed}, z={initial_z_transformed}")
else:
    print("Erreur de lecture de la position initiale. Veuillez vérifier les connexions.")
    exit()
    
# Lire la position 2000 ms
print("Lecture de la position pour 2000 ms...")
operate_valve_and_read_position(0, 2000)
time.sleep(5)
operate_valve_and_read_position(1, 2000)
time.sleep(5)
operate_valve_and_read_position(2, 2000)

# Attendre 1 seconde après la fermeture de toutes les valves pour lire les coordonnées
time.sleep(2)
test_error_x, test_error_y, test_error_z = paul.read_imu_data()

paul.write_one_valve_millis(0, -10000)
paul.write_one_valve_millis(1, -10000)
paul.write_one_valve_millis(2, -10000)
time.sleep(10)

if test_error_x is not None and test_error_y is not None and test_error_z is not None:
    # Appliquer la transformation des axes sur la position à 2000 ms
    new_x = -test_error_z  # Z devient -X
    new_y = -test_error_y  # Y devient -Y
    new_z = -test_error_x  # X devient -Z

    test_error_x_transformed = new_x - initial_x_transformed
    test_error_y_transformed = new_y - initial_y_transformed
    test_error_z_transformed = new_z - initial_z_transformed
    
    test_error_position_coords = (test_error_x_transformed, test_error_y_transformed, test_error_z_transformed)
    print(f"Position à 2000 ms définie à : x={test_error_x_transformed}, y={test_error_y_transformed}, z={test_error_z_transformed}")
else:
    print("Erreur de lecture de la position à 2000 ms. Veuillez vérifier les connexions.")
    exit()
# Générer des valeurs aléatoires uniques pour les durées d'ouverture des valves
def generate_unique_random_values(n, lower_bound=0, upper_bound=2000):
    unique_values = set()
    while len(unique_values) < n:
        new_value = (random.randint(lower_bound, upper_bound),
                     random.randint(lower_bound, upper_bound),
                     random.randint(lower_bound, upper_bound))
        unique_values.add(new_value)
    return list(unique_values)

# Préparation du fichier CSV
csv_filename = "positions_data.csv"
csv_headers = ['Valve0_duration', 'Valve1_duration', 'Valve2_duration', 'X', 'Y', 'Z']

try:
    # Créer et ouvrir le fichier CSV pour écrire les données
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_headers)  # Écrire les en-têtes
        print("En-têtes écrites dans le fichier CSV.")

        # La première position est fixée à (2000, 2000, 2000)
        test_error_position = (2000, 2000, 2000)

        # Générer 999 positions aléatoires uniques pour les durées d'ouverture des valves
        random_positions = generate_unique_random_values(1000)  # Fonction qui retourne une liste de tuples aléatoires

        # Combiner la position initiale avec les positions aléatoires pour créer la liste complète
        positions = [test_error_position] + random_positions

        # Processus principal
        for i, position in enumerate(positions):
            # Chaque 10 itérations, vérifier la position initiale
            if i > 0 and i % 10 == 0:
                print(f"Vérification périodique à l'itération {i}...")
                operate_valve_and_read_position(0, 2000)
                time.sleep(5)
                operate_valve_and_read_position(1, 2000)
                time.sleep(5)
                operate_valve_and_read_position(2, 2000)

                # Attendre 1 seconde après la fermeture de toutes les valves pour lire les coordonnées
                time.sleep(2)
                x, y, z = paul.read_imu_data()
                paul.write_one_valve_millis(0, -10000)
                paul.write_one_valve_millis(1, -10000)
                paul.write_one_valve_millis(2, -10000)
                time.sleep(10)

                if x is None or y is None or z is None:
                    print("Erreur de lecture des données IMU pendant la vérification.")
                    csv_writer.writerow([2000, 2000, 2000, "Il y a un problème"])
                    break

                # Appliquer la transformation des axes sur les nouvelles données
                new_x = -z
                new_y = -y
                new_z = -x
                 # Calculer les positions relatives par rapport à la position initiale transformée
                relative_x = new_x - initial_x_transformed
                relative_y = new_y - initial_y_transformed
                relative_z = new_z - initial_z_transformed

                # Vérifier les coordonnées avec une tolérance de +/- 4 degrés
                if not (abs(relative_x - test_error_x_transformed) <= 3 and
                        abs(relative_y - test_error_y_transformed) <= 3):
                    print("Le ballon a explosé.")
                    csv_writer.writerow([2000, 2000, 2000, "le ballon a explosé"])
                    break

                # Si la vérification est réussie, écrire les coordonnées dans le fichier CSV
                #csv_writer.writerow([2000, 2000, 2000, relative_x, relative_y, relative_z])
                print("Vérification réussie, les positions sont stables.")
                continue  # Passer à l'itération suivante

            # Gonfler les ballons selon les durées définies dans `position`
            valve0_duration, valve1_duration, valve2_duration = position

            # Opérer sur chaque valve et lire la position
            operate_valve_and_read_position(0, valve0_duration)
            time.sleep(5)
            operate_valve_and_read_position(1, valve1_duration)
            time.sleep(5)
            operate_valve_and_read_position(2, valve2_duration)

            # Attendre 1 seconde après la fermeture de toutes les valves pour lire les coordonnées
            time.sleep(2)

            # Lire la nouvelle position
            x, y, z = paul.read_imu_data()
            paul.write_one_valve_millis(0, -10000)
            paul.write_one_valve_millis(1, -10000)
            paul.write_one_valve_millis(2, -10000)
            time.sleep(10)

            if x is not None and y is not None and z is not None:
                # Appliquer la transformation des axes sur les nouvelles données
                new_x = -z
                new_y = -y
                new_z = -x
                # Calculer les positions relatives par rapport à la position initiale transformée
                relative_x = new_x - initial_x_transformed
                relative_y = new_y - initial_y_transformed
                relative_z = new_z - initial_z_transformed

                # Écrire les données dans le fichier CSV
                csv_writer.writerow([valve0_duration, valve1_duration, valve2_duration, relative_x, relative_y, relative_z])
                print(f"Données écrites dans le fichier CSV : Valve0={valve0_duration}, Valve1={valve1_duration}, Valve2={valve2_duration}, X={relative_x}, Y={relative_y}, Z={relative_z}")
            else:
                print("Impossible de lire les données IMU après manipulation des valves.")

except IOError as e:
    print(f"Erreur lors de l'ouverture/écriture du fichier CSV : {e}")

finally:
    paul.close()  # Assurer que la connexion série est fermée proprement
    print("Connexion série fermée et fichier CSV fermé.")