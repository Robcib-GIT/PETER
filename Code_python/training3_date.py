from tensorflow import keras
import numpy as np
import csv
import os

# Directoire de travail
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

# Définir les paramètres du modèle
input_size = 2  # Nombre de caractéristiques d'entrée (features)
hidden_units = 128  # Nombre d'unités dans la couche cachée
output_units = 3  # Nombre d'unités de sortie (3 pour chaque valve)

# Définir l'architecture du réseau de neurones
model = keras.Sequential([
    keras.layers.Input(shape=(input_size,)),  # Couche d'entrée

    # Couche cachée avec activation sigmoid
    keras.layers.Dense(units=hidden_units, activation='sigmoid'),

    # Couche de sortie avec activation linéaire
    keras.layers.Dense(units=output_units, activation=None)
])

# Charger les données du fichier CSV
times = np.zeros((1, 3), dtype=int)
positions = np.zeros((1, 2), dtype=float)

with open(curr_dir + 'positions1_data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        float_values = [float(x) for x in row]
        times = np.vstack([times, [float_values[:3]]])
        positions = np.vstack([positions, float_values[3:5]])

# Supprimer la première ligne de zéros
times = times[1:]
positions = positions[1:]

# Compiler le modèle
model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['accuracy'])

# Afficher le résumé du modèle
model.summary()

# Diviser les données en ensembles d'entraînement et de test
times_train = times[:-20]
times_test = times[-20:]
positions_train = positions[:-20]
positions_test = positions[-20:]

# Définir un callback pour imprimer les prédictions et les valeurs réelles après chaque epoch
class PrintPredictions(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if epoch % 10 == 0:  # Imprimer tous les 10 epochs
            predictions = self.model.predict(positions_test)
            print(f"Après l'epoch {epoch + 1} :")
            for i in range(len(predictions)):
                predicted = predictions[i]
                true = times_test[i]
                
                # Calcul de l'erreur en millisecondes
                errors = np.abs(predicted - true)
                
                print(f"Prédit : {predicted} \t Réel : {true} \t Erreurs (ms) : {errors}")

# Entraîner le modèle
model.fit(positions_train, times_train, epochs=10000, callbacks=[PrintPredictions()])

# Évaluer le modèle
test_loss, test_acc = model.evaluate(positions_test, times_test, verbose=2)
print(f"Précision du test : {test_acc}")

# Sauvegarder le modèle
model.save(curr_dir + 'pos2time_model.keras')
