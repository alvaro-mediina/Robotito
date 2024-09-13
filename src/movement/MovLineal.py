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
motor = Motor(giro,encoder)

#Indico distancia a mover en CM
distancia = 50
pulsos = round(distancia/theorical_move_per_pulse)

encoder.iniciar_cuenta()
#El motor de la izquierda va más lento que el de la derecha
motor.avanzar(50,62) #(DER|IZQ)
time.sleep(pulsos/for_DutyCycle_50) #10 es para este ciclo de trabajo
motor.stop()
contador1,contador2 = encoder.detener_cuenta()
distancia_med_enc = (((contador1 + contador2)/2)*theorical_move_per_pulse)/10
print("Distancia medida por Encoder: ",round(distancia_med_enc,2), " cm")
        
#motor.stop()


