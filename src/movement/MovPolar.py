import time
import sys
import RPi.GPIO as GPIO

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder
from constants import *
from RPi_map import *
import matplotlib.pyplot as plt
from calc_errores import calc_errores

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

encoder = Encoder()
giro = Mpu6050()
print(giro.get_temp())
motor = Motor(giro,encoder)

motor.stop()

#Indico angulo a rotar en grados
angulo = 90
distancia = 50


#motor.rotate(angulo)
#time.sleep(5)
#pulsos = round(distancia/theorical_move_per_pulse)
#motor.avanzar(50,62) #(DER|IZQ)
#time.sleep(pulsos/for_DutyCycle_50) #10 es para este ciclo de trabajo
#motor.stop()
motor.polar_control(angulo,distancia)

#contador1, contador2 = motor.polar_control(angulo,distancia)
#distancia_med_enc = (((contador1 + contador2)/2)*theorical_move_per_pulse)/10
#print("Distancia medida por Encoder: ",round(distancia_med_enc,2), " cm")




