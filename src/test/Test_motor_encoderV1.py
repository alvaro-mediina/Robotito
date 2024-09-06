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


motor = Motor(giro,encoder)
encoder.iniciar_cuenta()

flag = False

while  not flag:
    motor.avanzar(0,50)
    contadorA0, contadorB0 = encoder.obtener_pulsos()
    
    contadorA0 = abs(contadorA0)
    contadorB0 = abs(contadorB0)
    
    if contadorA0 > pulse_per_lap:
        GPIO.output(CLKWA0,0) #Si dio "una vuelta" apago el motor izquierda.
    if contadorB0 > pulse_per_lap:
        GPIO.output(CLKWB0,0) #Si dio "una vuelta" apago el motor derecha.
    
    if contadorA0 >= pulse_per_lap or contadorB0 >= 75:
        flag = True

motor.stop()
encoder.detener_cuenta()
        
        
#motor.stop()

