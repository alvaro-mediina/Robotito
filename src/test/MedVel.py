import time
import sys
import RPi.GPIO as GPIO
import statistics
import matplotlib.pyplot as plt

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder
from RPi_map import *
from threading import Lock
from calc_errores import calc_errores
from constants import *

scan_data_lock = Lock()
# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

#Definiciones
encoder = Encoder()
giro = Mpu6050()
print("Sensores creados")
motor = Motor(giro,encoder)
motor.stop()
encoder.iniciar_cuenta()

#Array velocidades
arr_vel_enc1 = []
arr_vel_enc2 = []

#Constantes
tiempo = 0.1
cnt = 0
dutyCycle = 90

#Iteraciones
iterac = 20

#Caso Base
cnt1_ant = 0
cnt2_ant = 0

motor.avanzar(dutyCycle,dutyCycle)

while cnt < iterac:
    
    #Obtengo pulsos
    time.sleep(tiempo)
    contador1, contador2 = encoder.obtener_pulsos()
    
    #Diferencias de Pulsos   
    diff_pulsos1 = contador1 - cnt1_ant  
    diff_pulsos2 = contador2 - cnt2_ant
    
    #Desplazamientos
    desp_enc1 = diff_pulsos1 * theorical_move_per_pulse
    desp_enc2 = diff_pulsos2 * theorical_move_per_pulse
    
    #Velocidades
    vel_enc1 = desp_enc1/tiempo
    vel_enc2 = desp_enc2/tiempo
    
    arr_vel_enc1.append(vel_enc1)
    arr_vel_enc2.append(vel_enc2)
    
    cnt1_ant = contador1
    cnt2_ant = contador2
    cnt += 1

encoder.detener_cuenta()
motor.stop()


promedio_enc1 = statistics.mean(arr_vel_enc1)
promedio_enc2 = statistics.mean(arr_vel_enc2)

promedio_enc1 = round(promedio_enc1,2)
promedio_enc2 = round(promedio_enc2,2)

print("Promedio ENC1: ", promedio_enc1, "mm/seg")
print("Promedio ENC2: ", promedio_enc2, "mm/seg")

fig, ax = plt.subplots(figsize=(3,3))
ax.plot(arr_vel_enc1, linewidth=2 ,color="red", label="Encoder 1")
ax.plot(arr_vel_enc2, linewidth=2 ,color="blue", label="Encoder 2")
ax.set(xlim=(0, iterac-1))
ax.set_xlabel("Iteraciones")
ax.set_ylabel("Velocidades")
ax.set_title(f"Gráfica de las velocidades medidas por cada encoder para un mismo dutyCicle({dutyCycle})")
ax.legend()
plt.show()

