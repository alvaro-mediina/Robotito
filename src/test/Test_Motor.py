import time
import sys

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder

encoder = Encoder()
giro = Mpu6050()
print("Sensores creados")

#giro.calibrate()
motor = Motor(giro,encoder)
motor.avanzar(0,0)
time.sleep(5)
motor.stop()

    
