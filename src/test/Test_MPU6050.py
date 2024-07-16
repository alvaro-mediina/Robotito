import time
import sys
import matplotlib.pyplot as plt
from threading import Lock

sys.path.append("../utils/")
sys.path.append("../data/")

from Mpu6050 import Mpu6050
from Rplidar import Rplidar
from calc_errores import calc_errores

scan_data_lock = Lock()

#lidar = Rplidar(scan_data_lock,'/dev/ttyUSB0', display = True)
# Crear una instancia del sensor
giro = Mpu6050()
# Realizar la calibración
giro.calibrate()
error = calc_errores(giro)
error_accel = error[0]
error_incl = error[1]
error_gyro = error[2]
gyro_tot = 0
gyro_tot_array = []
cnt = 0
while cnt < 10:

    # Obtener datos de aceleración
    accel_data = giro.get_accel()
    # Obtener datos de inclinación
    inclination_data =  giro.get_inclination()
    # Obtener datos del giroscopio
    gyro_data = giro.get_gyro()
    
    #Corregir datos
    for i in range(3):
        accel_data[i] -= error_accel[i]
        if i < 2:
            inclination_data[i] -= error_incl[i]
        gyro_data[i] -= error_gyro[i]
    
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

#lidar.grafico_lidar()