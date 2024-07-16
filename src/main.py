import time
import sys
import matplotlib.pyplot as plt
from threading import Lock
import RPi.GPIO as GPIO

sys.path.append("./data/")
sys.path.append("./utils/")
sys.path.append("./movement/")

from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder
from Rplidar import Rplidar
from calc_errores import calc_errores

#scan_data_lock() = Lock()
#lidar = Rplidar()

encoder = Encoder()
giro = Mpu6050()
motor = Motor(giro,encoder)

giro.calibrate()
error = calc_errores(giro)
error_accel = error[0]
error_incl = error[1]
error_gyro = error[2]
gyro_tot = 0
gyro_tot_array = []
#Motor
encoder.iniciar_cuenta()

# Iniciar la cuenta de pulsos
encoder.iniciar_cuenta()
motor.avanzar(90,90)
time.sleep(2)

motor.stop()
time.sleep(2)

motor.avanzar(-90,-90)
time.sleep(2)

motor.stop()
encoder.detener_cuenta()

# Obtener la distancia recorrida
distancia1, distancia2 = encoder.obtener_distancia()
print("Distancia recorrida por la rueda del motor A (ENCODER_B1): {:.2f} mm".format(distancia1))
print("Distancia recorrida por la rueda del motor B (ENCODER_A0): {:.2f} mm".format(distancia2))

# Limpiar los GPIOs
GPIO.cleanup()