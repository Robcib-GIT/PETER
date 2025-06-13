import numpy as np
import matplotlib.pyplot as plt

# Parámetros
n_datos = 10000
media_deseada = 0.2
max_valor = 1.1

# Elegimos a > 1 para evitar acumulación en 0
a = 2
b = (a / media_deseada) - a

# Generamos los datos
datos = np.random.beta(a, b, n_datos) * max_valor

# Mostramos media y mediana
print(f"Media: {np.mean(datos):.4f}, Mediana: {np.median(datos):.4f}")
# Mostramos el máximo y el mínimo
print(f"Máximo: {np.max(datos):.4f}, Mínimo: {np.min(datos):.4f}")

# Dibujamos el histograma
plt.hist(datos, bins=20 , color='blue')
plt.xlabel('Error Total')
plt.ylabel('Frequency')
plt.title('Histogram of Error Total')
plt.show()
