"""
PETER_trainning_NN.py
Mar Martín Díaz
"""
import os 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # Desactivar oneDNN custom operations
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import Input
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import joblib

# Cargar el archivo CSV
data = pd.read_csv('simulacion_random.csv')

# Separar las entradas (posicion del efector final) y salidas (tiempos de las válvulas)
X = data[['Final_Effector_X', 'Final_Effector_Y', 'Final_Effector_Z']]
y = data[['Valve1_0', 'Valve1_1', 'Valve1_2', 'Valve2_0', 'Valve2_1', 'Valve2_2']]

# Asegurarse de que y está en el rango correcto
y = y.clip(0, 2000)

# Normalizar las entradas
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Dividir los datos en conjunto de entrenamiento (90%) y prueba (10%)
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.1, random_state=42)

# Crear modelo secuencial de Keras
model = Sequential([
    Input(shape=(3,)),  
    Dense(256, activation='gelu', kernel_regularizer=l2(0.01)),
    Dropout(0.3),
    Dense(128, activation='gelu', kernel_regularizer=l2(0.01)),
    Dropout(0.3),
    Dense(64, activation='gelu', kernel_regularizer=l2(0.01)),
    Dropout(0.3),
    Dense(32, activation='gelu', kernel_regularizer=l2(0.01)),
    Dense(6)
])

# Compilar el modelo con Nadam optimizer
model.compile(optimizer=tf.keras.optimizers.Nadam(learning_rate=0.001), loss='mse')

# Configurar los callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True) # Detener el entrenamiento si la pérdida de validación no mejora después de 20 épocas, restaurando los mejores pesos
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=10, min_lr=1e-6) # Reducir la tasa de aprendizaje si la pérdida de validación no mejora después de 10 épocas

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=250, batch_size=32, validation_split=0.15, 
                    callbacks=[early_stopping, reduce_lr])

# Evaluar el modelo con el conjunto de prueba
loss = model.evaluate(X_test, y_test)

# Guardar el modelo
model.save('modelo_entrenado_optimizado.keras')

# Guardar el escalador
joblib.dump(scaler, 'scaler.pkl')

# Dibujar función de pérdida
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Loss function')
plt.show()

