import time
import sys
import RPi.GPIO as GPIO

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder
from constants import pulse_per_lap
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

#Realizar la calibración de la MPU
giro.calibrate()
error = calc_errores(giro)
error_gyro = error[2]
gyro_tot_enc = 0
gyro_tot_enc_array = []
gyro_tot_mpu = 0
gyro_tot_mpu_array = []



cnt = 0

tiempo = 0.1

motor = Motor(giro,encoder)
motor.stop()
encoder.iniciar_cuenta()


while cnt < 1000:
    time.sleep(tiempo)
    # Obtener y corregir datos del giroscopio
    gyro_data = giro.get_gyro()
    gyro_data[2] -= error_gyro[2]
    
    #print("Rotacion Temp: %f"%velocidades[2])
    #print("Rotacion accum: %f"%self.rotacion)
    #print(velocidades)
    
    gyro_tot_mpu = gyro_tot_mpu + gyro_data[2]*0.1
    gyro_tot_mpu_array.append(gyro_tot_mpu)
    
    contador1, contador2 = encoder.obtener_pulsos()
    
    #Velocidades de las ruedas
    vel_angular_prom_B1 = (360*contador1)/(pulse_per_lap*tiempo)
    vel_angular_prom_A0 = (360*contador2)/(pulse_per_lap*tiempo)
    vel_angular_prom = (-vel_angular_prom_B1 + vel_angular_prom_A0)/13
    
    gyro_tot_enc = (tiempo*vel_angular_prom*3)/3
    gyro_tot_enc_array.append(gyro_tot_enc)
    
    cnt += 1

encoder.detener_cuenta()

fig, ax = plt.subplots(figsize=(3,3))
ax.plot(gyro_tot_enc_array, linewidth=2 ,color="red", label="Encoder")
ax.plot(gyro_tot_mpu_array, linewidth=2 ,color="blue", label="MPU")
ax.set(xlim=(0, cnt))
ax.set_xlabel("Iteraciones")
ax.set_ylabel("Grados")
ax.set_title("Gráfica del giro total en el eje Z")
ax.legend()
plt.show()



