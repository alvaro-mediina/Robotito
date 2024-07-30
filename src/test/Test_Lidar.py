import time
import sys
import matplotlib.pyplot as plt
from threading import Lock

sys.path.append("../utils/")
sys.path.append("../data/")

from Rplidar import Rplidar

scan_data_lock = Lock()
lidar = Rplidar(scan_data_lock,'/dev/ttyUSB0', display = True)

lidar_x,lidar_y = lidar.get_valores_lidar()

fig, ax = plt.subplots(figsize=(3,3))
ax.plot(lidar_x, lidar_y, linewidth=2 ,color="red")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Mapa de obstaculos generado por RPLIDAR")
ax.legend()
plt.show()