import time
import sys
import matplotlib.pyplot as plt
from threading import Lock

sys.path.append("../utils/")

from Mpu6050 import Mpu6050
from Rplidar import Rplidar

def calc_errores(giro):
    scan_data_lock = Lock()
    #lidar = Rplidar(scan_data_lock,'/dev/ttyUSB0', display = True)
    # Realizar la calibración
    giro.calibrate()
    gyro_tot = 0
    gyro_tot_array = []
    cnt = 0
    sum_accel = [0.0,0.0,0.0]
    sum_incl = [0.0,0.0]
    sum_gyro = [0.0,0.0,0.0]
    while cnt < 200:
    
        # Obtener y mostrar datos de aceleración
        accel_data = giro.get_accel()
        # Obtener y mostrar datos de inclinación
        inclination_data =  giro.get_inclination()
        # Obtener y mostrar datos del giroscopio
        gyro_data = giro.get_gyro()

        gyro_tot = gyro_tot + gyro_data[2]*0.005
        gyro_tot_array.append(gyro_tot)
    
        for i in range(3):
            if i == 2:
                sum_accel[i] += (accel_data[i] - 1)
            else:
                sum_accel[i] += accel_data[i]
            if i < 2:
                sum_incl[i] += inclination_data[i]
            sum_gyro[i] += gyro_data[i]
        time.sleep(0.02)
        cnt += 1

    for i in range(3):
        sum_accel[i] *= 0.005
        if i < 2:
            sum_incl[i] *= 0.005
        sum_gyro[i] *= 0.005

    for i in range(3):
        accel_data[i] -= sum_accel[i]
        if i < 2:
            inclination_data[i] -= sum_incl[i]
        gyro_data[i] -= sum_gyro[i]

    print(f"Aceleración error [X, Y, Z]: {sum_accel}")
    print(f"Inclinación error [X, Y]: {sum_incl}")
    print(f"Giroscopio error [X, Y, Z]: {sum_gyro}")
    print("\n")

    #lidar.grafico_lidar()
    return sum_accel, sum_incl, sum_gyro