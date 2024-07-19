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

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

encoder = Encoder()
giro = Mpu6050()
print("Sensores creados")

#giro.calibrate()
motor = Motor(giro,encoder)
encoder.iniciar_cuenta()
motor.avanzar(80,90)
time.sleep(1.8)

motor.stop()
contador1, contador2 = encoder.detener_cuenta()
distancia1, distancia2 = encoder.obtener_distancia()
print("Distancia recorrida por la rueda del motor A (ENCODER_B1): {:.2f} mm".format(distancia1))
print("Distancia recorrida por la rueda del motor B (ENCODER_A0): {:.2f} mm".format(distancia2))
print("Velocidad angular promedio en canal ENCODER_B1: " + str((2*3.1415926*contador1)/(75*1.8)) + " rad/s")
print("Velocidad angular promedio en canal ENCODER_A0: " + str((2*3.1415926*contador2)/(75*1.8)) + " rad/s")
# Limpiar los GPIOs
GPIO.cleanup()
#time.sleep(2)

#motor.avanzar(-100,-100)
#time.sleep(2)
#motor.stop()


#print("Total de radianes en canal ENCODER_B1: " + str((2*3.1415926*self.contador1)/75))
#print("Total de radianes en canal ENCODER_A0: " + str((2*3.1415926*self.contador2)/75))
    
