import sys
import matplotlib.pyplot as plt
from threading import Lock
import time

sys.path.append("../utils/")
sys.path.append("../data/")

from Rplidar import Rplidar

scan_data_lock = Lock()
lidar = Rplidar(scan_data_lock,'/dev/ttyUSB1', display = True)
time.sleep(3)
#lidar.reset()
lidar_x,lidar_y = lidar.get_valores_lidar()
lidar.clear_input()

#print(lidar.angles)
#print(len(lidar.angles))

#plt.figure()
#plt.plot(lidar.angles, [1]*len(lidar.angles),'bo')
#plt.show()

fig, ax = plt.subplots(figsize=(3,3))
ax.plot(lidar_x, lidar_y,'o', linewidth=2 ,color="red")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Mapa de obstaculos generado por RPLIDAR")
ax.legend()
plt.show()
lidar.cleanup()
