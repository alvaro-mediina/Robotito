import time
import sys
import RPi.GPIO as GPIO

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder


# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

encoder = Encoder()
giro = Mpu6050()
print("Sensores creados")

motor = Motor(giro,encoder)

start = int(input("Avanzar ->"))

while start != 0:
    motor.avanzar(100,100)
    start = int(input("Avanzar -> "))

motor.stop()



