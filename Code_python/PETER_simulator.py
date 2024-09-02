"""
Simulador de PETER
Mar Martín Díaz
"""
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os


# CONSTANTES
initial_height = 47.0  # Altura inicial de cada actuador en mm
side_length = 170.0  # Longitud del lado del triángulo equilátero en mm
m = 31.0  # Pendiente altura-tiempo de hinchado (mm/ms)
module_gap = 17.0  # Separación entre módulos en mm (de actuador a actuador)
effector_dist = 17.0  # Distancia del efector final al último actuador en mm
base_height = 18.0 # Altura de la base del primer módulo en mm
num_modules = 2 # Número de módulos 

# Archivo simulacion.csv
# Columnas que debe tener el CSV
columns = [f'Valve{module + 1}_{i}' for module in range(num_modules) for i in range(3)]
columns += ['Final_Effector_X', 'Final_Effector_Y', 'Final_Effector_Z']

# Verificar si el archivo existe, si no, crearlo con las columnas 
if not os.path.isfile('simulacion.csv'):
    df = pd.DataFrame(columns=columns)
    df.to_csv('simulacion.csv', index=False)

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

# Función para actualizar el gráfico en función de los tiempos de hinchado y el número de módulos
def update_plot(valve_times, num_modules):
    global ax
    ax.clear()

    base_vertices = triangle_vertices(base_height, side_length)  # Base del primer módulo

    for module in range(num_modules):
        # Alturas de cada actuador
        h1 = actuator_height(valve_times[module][0])
        h2 = actuator_height(valve_times[module][1])
        h3 = actuator_height(valve_times[module][2])

        # Dibujar la base
        for i in range(3):
            ax.plot([base_vertices[i, 0], base_vertices[(i + 1) % 3, 0]], 
                    [base_vertices[i, 1], base_vertices[(i + 1) % 3, 1]], 
                    [base_vertices[i, 2], base_vertices[(i + 1) % 3, 2]], color='b')

        # Ajustar las alturas de los vértices superiores en función del hinchado de los actuadores
        top_vertices = base_vertices.copy()
        plane_normal = np.cross(base_vertices[1] - base_vertices[0], base_vertices[2] - base_vertices[0])
        plane_normal /= np.linalg.norm(plane_normal)

        for i, h in enumerate([h1, h2, h3]):
            top_vertices[i] = base_vertices[i] + plane_normal * h

        # Dibujar los actuadores perpendiculares a la base del módulo
        for i in range(3):
            ax.plot([base_vertices[i, 0], top_vertices[i, 0]], 
                    [base_vertices[i, 1], top_vertices[i, 1]], 
                    [base_vertices[i, 2], top_vertices[i, 2]], 'g--')

        # Dibujar el triángulo que forman los actuadores
        for i in range(3):
            ax.plot([top_vertices[i, 0], top_vertices[(i + 1) % 3, 0]], 
                    [top_vertices[i, 1], top_vertices[(i + 1) % 3, 1]], 
                    [top_vertices[i, 2], top_vertices[(i + 1) % 3, 2]], color='k')

        # Base del siguiente módulo
        base_vertices, normal_vector = calculate_next_base(top_vertices, module_gap)
        last_top_vertices = top_vertices.copy()

    # Calcular el centro del último triángulo
    centroid = np.mean(last_top_vertices, axis=0)

    # Desplazar el centro del último triángulo en la dirección del vector normal
    final_effector = centroid + normal_vector * effector_dist

    # Dibujar el punto en el centro del último triángulo y el punto del efector final
    ax.scatter(centroid[0], centroid[1], centroid[2], color='r', label='Centro del último triángulo')
    #ax.text(centroid[0], centroid[1], centroid[2], f'({centroid[0]:.2f}, {centroid[1]:.2f}, {centroid[2]:.2f})', color='red')
    ax.scatter(final_effector[0], final_effector[1], final_effector[2], color='g', label='Centro del efector final')
    ax.text(final_effector[0], final_effector[1], final_effector[2], f'({final_effector[0]:.2f}, {final_effector[1]:.2f}, {final_effector[2]:.2f})', color='green')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Simulación del Robot Blando PETER')
    ax.set_xlim([-250, 250])
    ax.set_ylim([-250, 250])
    ax.set_zlim([0, 300])
    ax.legend()
    canvas.draw()

    # Devolver las coordenadas del punto desplazado
    return final_effector

# Función para actualizar el gráfico en función de los valores de los sliders
def update(*args):
    valve_times = []
    for module in range(num_modules):
        times = [sliders[module*3 + i].get() for i in range(3)]
        valve_times.append(times)
    global last_final_effector
    last_final_effector = update_plot(valve_times, num_modules)

# Función para guardar los datos en un archivo CSV
def save_data():
    valve_times = []
    for module in range(num_modules):
        times = [sliders[module*3 + i].get() for i in range(3)]
        valve_times.append(times)

    # Crear un DataFrame con los datos
    data = {}

    for module in range(num_modules):
        for i in range(3):
            data[f'Valve{module + 1}_{i}'] = [valve_times[module][i]]
            data['Final_Effector_X'] = [last_final_effector[0]]
            data['Final_Effector_Y'] = [last_final_effector[1]]
            data['Final_Effector_Z'] = [last_final_effector[2]]
    
    df = pd.DataFrame(data)
    
    # Guardar el DataFrame en el CSV 
    with open('simulacion.csv', mode='a', newline='') as file:
        df.to_csv(file, header=not os.path.isfile('simulacion.csv'), index=False)


def setup_ui():
    for i in range(num_modules * 3):
        frame = tk.Frame(frame_controls)
        frame.pack(fill=tk.X)
        label = tk.Label(frame, text=f"Valve {i + 1}")
        label.pack(side=tk.LEFT)
        slider = tk.Scale(frame, from_=0, to=2000, orient=tk.HORIZONTAL, command=lambda val, i=i: entries[i].delete(0, tk.END) or entries[i].insert(0, val))
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)
        entry.bind("<Return>", lambda event, i=i: sliders[i].set(entries[i].get()))
        sliders.append(slider)
        entries.append(entry)

    # Crear botones
    button_update = tk.Button(frame_controls, text="Actualizar simulación", command=update)
    button_update.pack(pady=5)
    button_save = tk.Button(frame_controls, text="Guardar datos", command=save_data)
    button_save.pack(pady=5)

root = tk.Tk()
root.title("Control de válvulas de PETER")

frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

sliders = []
entries = []

setup_ui()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

update()
root.mainloop()

