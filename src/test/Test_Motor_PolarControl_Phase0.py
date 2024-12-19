import time
import sys
import statistics
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

encoder = Encoder()
giro = Mpu6050()
motor = Motor(giro,encoder)

archivo = 'Datos_LinearControl.txt'

#Limpieza
cleanFile(archivo)

#Mega-Panic
#iniciar = 0

iniciar = int(input("¿Comenzar? -> "))
 
while iniciar != 0 :
    if iniciar == 1:
        #Calibración
        motor.calibrate_wheels()
    elif iniciar == 2:
        datos = motor.linear_control_med(700)
        # Llamada a la función
        write(archivo, datos)
        vel_enc1, vel_enc2, errors = parse_file_to_list_of_lists(archivo)
        error_indices = list(range(2, len(vel_enc1), 3))
        err1_values = [error[0] for error in errors]
        err2_values = [error[1] for error in errors]
        plot_velocity_and_errors(vel_enc1, vel_enc2, err1_values, err2_values, error_indices)

    elif iniciar == 3:
        #Calibracion de la MPU
        motor.calibrate_gyro()
        motor.linear_control_med(700)
        
    iniciar = int(input("¿Ahora? -> "))
    
if iniciar == 0:
    #Panic
    motor.stop()
