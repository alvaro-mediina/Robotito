import time
import sys
import RPi.GPIO as GPIO

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from array_writer_file import write
from ParseFiletoList import *
from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder
from constants import *
from RPi_map import *
import matplotlib.pyplot as plt
from calc_errores import calc_errores

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

#Defs
encoder = Encoder()
giro = Mpu6050()
motor = Motor(giro,encoder)

#Limpieza
#cleanFile(archivo)

#Panic
#motor.stop()


value = int(input("¿Comenzar? -> "))
#value = 0
while value != 0 :
    if value == 1:
        #Calibracion
        motor.calibrate_wheels()
    elif value == 2:
        motor.rotate_with_timer(90)
    value = int(input("Ahora? -> "))

if value == 0 :
    print("Control terminado")
    #Panic
    motor.stop()
    exit() 