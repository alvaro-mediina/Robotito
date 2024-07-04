import time
import sys
import matplotlib.pyplot as plt
from threading import Lock

sys.path.append("../utils/")
sys.path.append("../data/")

from Mpu6050 import Mpu6050
from Rplidar import Rplidar

scan_data_lock = Lock()

lidar = Rplidar(scan_data_lock,'/dev/ttyUSB1', display = True)
# Crear una instancia del sensor
giro = Mpu6050()
# Realizar la calibración
giro.calibrate()
gyro_tot = 0
gyro_tot_array = []
cnt = 0
while cnt < 10:

    # Obtener y mostrar datos de aceleración
    accel_data = giro.get_accel()
    # Obtener y mostrar datos de inclinación
    inclination_data =  giro.get_inclination()
    # Obtener y mostrar datos del giroscopio
    gyro_data = giro.get_gyro()
    
    gyro_tot = gyro_tot + gyro_data[2]*0.1
    gyro_tot_array.append(gyro_tot)
    
    print(f"Aceleración [X, Y, Z]: {accel_data}")
    print(f"Inclinación [X, Y]: {inclination_data}")
    print(f"Giroscopio [X, Y, Z]: {gyro_data}")
    print(f"Giroscopio Total [Z]: {gyro_tot}")
    print("\n")
    time.sleep(0.1)
    cnt += 1


plt.plot(gyro_tot_array)
plt.show()

lidar.grafico_lidar()