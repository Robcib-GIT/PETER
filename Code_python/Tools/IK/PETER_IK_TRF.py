"""
PETER_IK_TRF.py
Mar Martín Díaz
"""
import numpy as np
from scipy.optimize import least_squares
import tkinter as tk

# CONSTANTES
initial_height = 47.0  # Altura inicial de cada actuador en mm
side_length = 170.0  # Longitud del lado del triángulo equilátero en mm
m = 31.0  # Pendiente altura-tiempo de hinchado (mm/ms)
module_gap = 17.0  # Separación entre módulos en mm (de actuador a actuador)
effector_dist = 17.0  # Distancia del efector final al último actuador en mm
base_height = 18.0 # Altura de la base del primer módulo en mm
num_modules = 1 # Número de módulos 


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

# Función para calcular la posición del efector final en función de los tiempos de hinchado
def calculate_effector_position(valve_times):
    base_vertices = triangle_vertices(base_height, side_length)  # Base del primer módulo

    for module in range(num_modules):
        # Alturas de cada actuador
        h1 = actuator_height(valve_times[module][0])
        h2 = actuator_height(valve_times[module][1])
        h3 = actuator_height(valve_times[module][2])

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
    displaced_centroid = centroid + normal_vector * effector_dist

    return displaced_centroid

# Función para resolver la cinemática inversa con Trust Region Reflective
def IK_TRF(target):

    bounds = (np.zeros((num_modules * 3)), np.ones((num_modules * 3)) * 2000)
    result = least_squares(residuals_function, np.ones((num_modules * 3)) * 1000, bounds=bounds, args=(target,), max_nfev=2000, method='trf')
    
    # Redondear los resultados al entero más cercano
    refined_solution = np.round(result.x)
    return refined_solution.reshape((num_modules, 3))

# Función de residuos para el algoritmo de Trust Region Reflective
def residuals_function(valve_times, target):
    valve_times = valve_times.reshape((num_modules, 3))
    result = calculate_effector_position(valve_times)
    return (result - target).flatten()

# Interfaz gráfica de usuario 
def on_calculate_button_clicked():
    target_x = float(target_x_entry.get())
    target_y = float(target_y_entry.get())
    target_z = float(target_z_entry.get())
    
    target = np.array([target_x, target_y, target_z])
    
    valve_times = IK_TRF(target)

    real_pos = calculate_effector_position(valve_times)
    real_pos = np.round(real_pos, 2)
    real_results.config(text=f"x={real_pos[0]}, y={real_pos[1]}, z={real_pos[2]}")
    
    print("Valve times:", valve_times)  
    
    if valve_times.shape != (num_modules, 3):
        print("Error: valve_times no tiene la forma correcta:", valve_times.shape)
        return
    
    for i in range(num_modules):
        for j in range(3):
            valve_entries[i*3 + j].delete(0, tk.END)
            valve_entries[i*3 + j].insert(0, str(int(valve_times[i][j])))

# Configurar la ventana principal
root = tk.Tk()
root.title("Cinemática Inversa")

# Crear widgets de entrada para los valores objetivo
target_x_label = tk.Label(root, text="Target X:")
target_x_label.grid(row=0, column=0)
target_x_entry = tk.Entry(root)
target_x_entry.grid(row=0, column=1)

target_y_label = tk.Label(root, text="Target Y:")
target_y_label.grid(row=1, column=0)
target_y_entry = tk.Entry(root)
target_y_entry.grid(row=1, column=1)

target_z_label = tk.Label(root, text="Target Z:")
target_z_label.grid(row=2, column=0)
target_z_entry = tk.Entry(root)
target_z_entry.grid(row=2, column=1)

# Botón para calcular
calculate_button = tk.Button(root, text="Calcular", command=on_calculate_button_clicked)
calculate_button.grid(row=4, columnspan=2, pady=(10, 10))

# Crear widgets para mostrar los resultados de los tiempos de hinchado
valve_entries = []
for i in range(num_modules * 3):
    valve_label = tk.Label(root, text=f"Valve {i+1}:")
    valve_label.grid(row=i+5, column=0)
    valve_entry = tk.Entry(root)
    valve_entry.grid(row=i+5, column=1)
    valve_entries.append(valve_entry)

# Resultados reales
real_label = tk.Label(root, text="Reached:")
real_label.grid(row = num_modules * 3 + 5, column = 0)
real_results = tk.Label(root, text="x=0, y=0, z=0")
real_results.grid(row = num_modules * 3 + 5, column = 1)

# Ejecutar la interfaz gráfica
root.mainloop()

