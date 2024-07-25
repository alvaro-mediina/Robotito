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

# Obtener datos iniciales del giroscopio
gyro_data_inicial = giro.get_gyro()
    
#Corregir datos
for i in range(3):
    gyro_data_inicial[i] -= error_gyro[i]

motor = Motor(giro,encoder)
encoder.iniciar_cuenta()
motor.avanzar(100,-100)
tiempo = 1
time.sleep(tiempo)

motor.stop()

# Obtener datos finales del giroscopio
gyro_data_final = giro.get_gyro()
    
#Corregir datos
for i in range(3):
    gyro_data_final[i] -= error_gyro[i]

contador1, contador2 = encoder.detener_cuenta()
distancia1, distancia2 = encoder.obtener_distancia()
#print("Distancia recorrida por la rueda del motor A (ENCODER_B1): {:.2f} mm".format(distancia1))
#print("Distancia recorrida por la rueda del motor B (ENCODER_A0): {:.2f} mm".format(distancia2))
vel_angular_prom_B1 = (360*contador1)/(75*tiempo)
vel_angular_prom_A0 = (360*contador2)/(75*tiempo)
vel_angular_prom = (vel_angular_prom_B1 + vel_angular_prom_A0)/2
#print("Velocidad angular promedio en canal ENCODER_B1: " + str(vel_angular_prom_B1) + " grados/s")
#print("Velocidad angular promedio en canal ENCODER_A0: " + str(vel_angular_prom_A0) + " grados/s")
#calculamos la rotacion en grados a partir de lo medido por los encoders
rotacion = (tiempo*2*3.1415926*vel_angular_prom*30)/(3.1415926*260) #Medir bien ese 260
print("Rotacion total medida por los encoders: " + str(rotacion))
gyro_tot = gyro_data_final[2] - gyro_data_inicial[2]
print(f"Rotacion total medida por la MPU: {gyro_tot}")
# Limpiar los GPIOs
GPIO.cleanup()
#time.sleep(2)

#motor.avanzar(-100,-100)
#time.sleep(2)
#motor.stop()


#print("Total de radianes en canal ENCODER_B1: " + str((2*3.1415926*self.contador1)/75))
#print("Total de radianes en canal ENCODER_A0: " + str((2*3.1415926*self.contador2)/75))
    
