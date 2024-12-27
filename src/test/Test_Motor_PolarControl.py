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
from Tools import *

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

encoder = Encoder()
giro = Mpu6050()
motor = Motor(giro,encoder)
counter = 1
array_coord = [(0,550),(90,550),(180,550)]

archivo = 'Datos_PolarControl.txt'

#Limpieza
cleanFile(archivo)

#Mega-Panic
#iniciar = 0

iniciar = int(input("¿Comenzar? -> "))

superMegaArrayReturn = []
while iniciar != 0 :
    if iniciar == 1:
        #Calibración
        motor.calibrate_wheels()
        motor.calibrate_gyro()
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
        phi = int(input("ÁNGULO ->"))
        dist = int(input("DISTANCIA ->"))
        if counter == 1:
            coord1 = (phi,dist)
            array_coord.append(coord1)
            counter += 1
        elif counter == 2:
            coord2 = (phi,dist)
            array_coord.append(coord2)
            counter += 1
        elif counter == 3:
            coord3 = (phi,dist)
            array_coord.append(coord3)
        superArrayReturn = motor.polarControl(phi, dist)
        for tupla in superArrayReturn:
            print(tupla)
            superMegaArrayReturn.append(tupla)
        print("Lenght superMegaArrayReturn -> ", len(superMegaArrayReturn) )
    elif iniciar == 4:
        phi = int(input("ÁNGULO ->"))
        motor.rotate_with_timer(phi)
        motor.giro.resetMPU()
    elif iniciar == 5:
        phi = int(input("ÁNGULO ->"))
        dist = int(input("DISTANCIA ->"))
        gyro_array = motor.polarControl(phi, dist)
        
        
    iniciar = int(input("¿Ahora? -> "))

print("Lenght superMegaArrayReturn -> ", len(superMegaArrayReturn) )

if type(superMegaArrayReturn) == type(array_coord):
    with open(archivo, "w", newline="") as archivo:
        for valor in superMegaArrayReturn:
            archivo.write(f"{valor} \n")
    #drawArrowsFromOrigin(array_coord, superMegaArrayReturn)
else:
    print("No tipea")
#drawAllData(superMegaArrayReturn, counter)

if iniciar == 0:
    #Panic
    motor.stop()

