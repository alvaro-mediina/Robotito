#75 pulsos por vuelta cada interrupcion
#60 mm de diametro c/ rueda
#2.512 mm avanzados de forma lineal por pulso medido
import time
import sys

sys.path.append("../utils/")
sys.path.append("../data/")

from RPi_map import *
import RPi.GPIO as GPIO


class Encoder():


    def __init__(self):
        
        self.contador1 = 0
        self.contador2 = 0    
    
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(ENCODER_A0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ENCODER_A1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ENCODER_B0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ENCODER_B1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Configurar la interrupción en el pin especificado (flanco de subida)
        GPIO.add_event_detect(ENCODER_B0, GPIO.RISING, callback=self.interrupcion_B_pos, bouncetime=30)
        GPIO.add_event_detect(ENCODER_A0, GPIO.RISING, callback=self.interrupcion_A_pos, bouncetime=30)

    #Cuenta la cantidad de pulsos generados por el encoder en cada rueda
    #Dependiendo del pin que generó el pulso.
    def obtener_pulsos(self):
        return self.contador1, self.contador2
    
    def interrupcion_B_pos(self, channel):
        if(GPIO.input(ENCODER_A1) == GPIO.HIGH):
            self.contador2 += 1
        else:
            self.contador2 -= 1

    def interrupcion_A_pos(self, channel):
        if(GPIO.input(ENCODER_B1) == GPIO.HIGH):
            self.contador1 += 1
        else:
            self.contador1 -= 1
        

    def iniciar_cuenta(self):
        self.contador1 = 0
        self.contador2 = 0
        print("Inicio de cuenta de pulsos.")

    # Método para detener la cuenta de pulsos
    def detener_cuenta(self):
        print("Total de pulsos en canal ENCODER_A0: " + str(self.contador2))
        print("Total de pulsos en canal ENCODER_B0: " + str(self.contador1))
        return self.contador1, self.contador2

    # Método para obtener la distancia recorrida en mm
    def obtener_distancia(self):
        distancia1 = self.contador1 * 2.512
        distancia2 = self.contador2 * 2.512
        return distancia1, distancia2


