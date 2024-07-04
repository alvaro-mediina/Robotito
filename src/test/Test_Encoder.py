import sys
import time
import RPi.GPIO as GPIO

sys.path.append("../utils/")
sys.path.append("../movement/")
sys.path.append("../data/")


from Encoder import Encoder
from RPi_map import *

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)


# Inicializar el encoder
encoder = Encoder()
flag = False

while flag != True :
    try:
        # Iniciar la cuenta de pulsos
        encoder.iniciar_cuenta()
        
        # Mantener el programa corriendo para contar los pulsos
        print("Presiona Ctrl+C para detener la cuenta.")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        # Detener la cuenta de pulsos
        encoder.detener_cuenta()
        # Obtener la distancia recorrida
        distancia1, distancia2 = encoder.obtener_distancia()
        print("Distancia recorrida por la rueda del motor A (ENCODER_B1): {:.2f} mm".format(distancia1))
        print("Distancia recorrida por la rueda del motor B (ENCODER_A0): {:.2f} mm".format(distancia2))
        
        # Limpiar los GPIOs
        GPIO.cleanup()
        flag = True

