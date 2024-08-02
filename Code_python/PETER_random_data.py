"""
PETER_random_data.py
Mar Martín Díaz
"""
import numpy as np
import pandas as pd

# CONSTANTES
initial_height = 47.0  # Altura inicial de cada actuador en mm
side_length = 150.0  # Longitud del lado del triángulo equilátero en mm
m = 31.0  # Pendiente altura-tiempo de hinchado (mm/ms)
module_gap = 19.0  # Separación entre módulos en mm (de actuador a actuador)
effector_dist = 5  # Distancia del efector final al último actuador en mm
num_modules = 2  # Número de módulos 
num_simulations = 10000  # Número de simulaciones

# Función para calcular la altura del actuador en función del tiempo de hinchado (en ms)
def actuator_height(inflation_time):
    return initial_height + (m * inflation_time / 2000)

# Función para calcular la posición de los vértices de un triángulo equilátero
def triangle_vertices(z, side_length):
    angle = np.linspace(0, 2 * np.pi, 4)[:3]
    x = side_length * np.cos(angle)
    y = side_length * np.sin(angle)
    return np.vstack((x, y, np.full(3, z))).T

# Función para calcular la nueva base del siguiente módulo
def calculate_next_base(current_top, module_gap):
    normal_vector = np.cross(current_top[1] - current_top[0], current_top[2] - current_top[0])  # Calcular el vector normal al plano de la tapa superior
    normal_vector = normal_vector / np.linalg.norm(normal_vector)  # Normalizar el vector
    
    # Desplazar la tapa superior hacia arriba en la dirección del vector normal
    next_base = current_top + normal_vector * module_gap
    return next_base, normal_vector

# Función para realizar una simulación y devolver las coordenadas del centroide desplazado
def simulate(valve_times):
    current_z = 5  # Inicializar la altura en z
    base_vertices = triangle_vertices(current_z, side_length)  # Base del primer módulo

    for module in range(num_modules):
        # Alturas de cada actuador
        h1 = actuator_height(valve_times[module * 3 + 0])
        h2 = actuator_height(valve_times[module * 3 + 1])
        h3 = actuator_height(valve_times[module * 3 + 2])

        # Ajustar las alturas de los vértices superiores en función del hinchado de los actuadores
        top_vertices = base_vertices.copy()
        plane_normal = np.cross(base_vertices[1] - base_vertices[0], base_vertices[2] - base_vertices[0])
        plane_normal /= np.linalg.norm(plane_normal)

        for i, h in enumerate([h1, h2, h3]):
            top_vertices[i] = base_vertices[i] + plane_normal * h

        # Base del siguiente módulo
        base_vertices, normal_vector = calculate_next_base(top_vertices, module_gap)
        last_top_vertices = top_vertices.copy()

    # Calcular el centro del último triángulo
    centroid = np.mean(last_top_vertices, axis=0)

    # Desplazar el centro del último triángulo en la dirección del vector normal
    final_effector = centroid + normal_vector * effector_dist

    # Devolver las coordenadas del punto desplazado
    return final_effector

# Generar datos aleatorios y calcular el centroide desplazado
data = []
for _ in range(num_simulations):
    valve_times = np.random.randint(0, 2000, num_modules * 3)  # Valores aleatorios entre 0 y 2000 para las válvulas
    final_effector = simulate(valve_times)
    data.append(np.concatenate((valve_times, final_effector)))

# Crear un DataFrame con los datos generados
columns = [f'Valve{module + 1}_{i}' for module in range(num_modules) for i in range(3)]
columns += ['Final_Effector_X', 'Final_Effector_Y', 'Final_Effector_Z']
df = pd.DataFrame(data, columns=columns)

# Guardar el DataFrame en un archivo CSV
df.to_csv('simulacion_random.csv', index=False)
