import time
import sys
import RPi.GPIO as GPIO

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder
from RPi_map import *
import matplotlib.pyplot as plt
from threading import Lock
from calc_errores import calc_errores

scan_data_lock = Lock()
# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

encoder = Encoder()
giro = Mpu6050()
print("Sensores creados")

tiempo = 0.1
cnt = 0

motor = Motor(giro,encoder)
motor.stop()
encoder.iniciar_cuenta()
cuenta_enc1_array = []
cuenta_enc2_array = []
motor.avanzar(90,90)

while cnt < 30:
    time.sleep(tiempo)
    contador1, contador2 = encoder.obtener_pulsos()
    cuenta_enc1_array.append(contador1)
    cuenta_enc2_array.append(contador2)
    cnt += 1

encoder.detener_cuenta()
motor.stop()

fig, ax = plt.subplots(figsize=(3,3))
ax.plot(cuenta_enc1_array, linewidth=2 ,color="red", label="Encoder 1")
ax.plot(cuenta_enc2_array, linewidth=2 ,color="blue", label="Encoder 2")
ax.set(xlim=(0, 30))
ax.set_xlabel("Iteraciones")
ax.set_ylabel("Pulsos")
ax.set_title("Gráfica de los pulsos medidos por cada encoder para un mismo ciclo de trabajo (90)")
ax.legend()
plt.show()