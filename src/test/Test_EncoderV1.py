import time
import sys
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

sys.path.append("../utils/")
sys.path.append("../data/")

from Encoder import Encoder
from RPi_map import *

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

# Inicializar el encoder
encoder = Encoder()

pulse_array_encA0 = []
pulse_array_encB0 = []

cnt = 0
tiempo = 0.1
print("Empezando a contar")
while cnt < 100:
    contadorA0, contadorB0 = encoder.obtener_pulsos()
    pulse_array_encA0.append(contadorA0)
    pulse_array_encB0.append(contadorB0)
    cnt += 1
    time.sleep(tiempo)
    
fig, ax = plt.subplots(figsize=(3,3))
ax.plot(pulse_array_encA0, linewidth=2 ,color="red", label="Encoder A")
ax.plot(pulse_array_encB0, linewidth=2 ,color="blue", label="Encoder B")
ax.set(xlim=(0, cnt))
ax.set_xlabel("Iteraciones")
ax.set_ylabel("Pulsos")
ax.set_title("Gráfica los pulsos detectados por cada Encoder")
ax.legend()
plt.show()
