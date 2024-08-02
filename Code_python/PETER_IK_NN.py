"""
PETER_IK_NN.py
Mar Martín Díaz
"""
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # Desactivar oneDNN custom operations
import numpy as np
import pandas as pd
import tensorflow as tf
import tkinter as tk
from tkinter import messagebox
import joblib

# Cargar el modelo y el escalador
model = tf.keras.models.load_model('modelo_entrenado_optimizado.keras')
scaler = joblib.load('scaler.pkl')

# Función para hacer predicciones
def make_prediction():
    try:
        x_coord = float(entry_x.get())
        y_coord = float(entry_y.get())
        z_coord = float(entry_z.get())

        input_data = pd.DataFrame([[x_coord, y_coord, z_coord]], columns=['Final_Effector_X', 'Final_Effector_Y', 'Final_Effector_Z'])
        input_data_normalized = scaler.transform(input_data)
        
        prediction = model.predict(input_data_normalized)
        prediction = np.clip(prediction, 0, 2000)  # Comprobar que las predicciones estén en el rango correcto
        
        for i in range(num_modules):
            for j in range(3):
                valve_labels[i*3 + j].config(text=f'Valve {i + 1}_{j}: {prediction[0][i*3 + j]:.2f} ms')
    except ValueError:
        messagebox.showerror("Entrada inválida", "Por favor, introduce coordenadas válidas.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("PETER IK con NN")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_x = tk.Label(frame_input, text="Coordenada X:")
label_x.grid(row=0, column=0, padx=5)
entry_x = tk.Entry(frame_input)
entry_x.grid(row=0, column=1, padx=5)

label_y = tk.Label(frame_input, text="Coordenada Y:")
label_y.grid(row=1, column=0, padx=5)
entry_y = tk.Entry(frame_input)
entry_y.grid(row=1, column=1, padx=5)

label_z = tk.Label(frame_input, text="Coordenada Z:")
label_z.grid(row=2, column=0, padx=5)
entry_z = tk.Entry(frame_input)
entry_z.grid(row=2, column=1, padx=5)

button_predict = tk.Button(root, text="Predecir", command=make_prediction)
button_predict.pack(pady=10)

frame_output = tk.Frame(root)
frame_output.pack(pady=10)

valve_labels = []
num_modules = 2  # Número de módulos

for i in range(num_modules):
    for j in range(3):
        label = tk.Label(frame_output, text=f'Valve {i + 1}_{j}:')
        label.pack()
        valve_labels.append(label)

root.mainloop()
