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
        GPIO.add_event_detect(ENCODER_B0, GPIO.RISING, callback=self.interrupcion)
        GPIO.add_event_detect(ENCODER_B1, GPIO.RISING, callback=self.interrupcion)
        GPIO.add_event_detect(ENCODER_A0, GPIO.RISING, callback=self.interrupcion)
        GPIO.add_event_detect(ENCODER_A1, GPIO.RISING, callback=self.interrupcion)

    #Cuenta la cantidad de pulsos generados por el encoder en cada rueda
    #Dependiendo del pin que generó el pulso.
    def obtener_pulsos(self):
        return self.contador1, self.contador2
    
    def interrupcion(self,channel):
        if channel == 31:
            self.contador1 += 1
            #if(self.contador1 >= 75):
                #print("Una vuelta \n")
            #print("Canal: " + str(ENCODER_B1) + ": " + str(self.contador1) + "\n")
        elif channel == 22:
            self.contador2 += 1
            #if(self.contador2 >= 75):
                #print("Una vuelta \n")
            #print("Canal: " + str(ENCODER_A0) + ": " + str(self.contador2) + "\n")
        

    # Método para iniciar la cuenta de pulsos
    def iniciar_cuenta(self):
        self.contador1 = 0
        self.contador2 = 0
        print("Inicio de cuenta de pulsos.")

    # Método para detener la cuenta de pulsos
    def detener_cuenta(self):
        print("Fin de cuenta de pulsos.")
        print("Total de pulsos en canal ENCODER_B1: " + str(self.contador1))
        print("Total de pulsos en canal ENCODER_A0: " + str(self.contador2))
        return self.contador1, self.contador2

    # Método para obtener la distancia recorrida en mm
    def obtener_distancia(self):
        distancia1 = self.contador1 * 2.512
        distancia2 = self.contador2 * 2.512
        return distancia1, distancia2


