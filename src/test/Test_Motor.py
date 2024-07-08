import time
import sys

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")

from Motor import Motor
from Mpu6050 import Mpu6050
from Encoder import Encoder

encoder = Encoder()
giro = Mpu6050()
print("Sensores creados")

#giro.calibrate()
motor = Motor(giro,encoder)
motor.avanzar(90,90)
time.sleep(2)

motor.stop()
time.sleep(2)

motor.avanzar(-90,-90)
time.sleep(2)
motor.stop()

    
