import RPi.GPIO as GPIO
import math
import statistics
import threading
import sys
import time
import random
from numpy import sign

sys.path.append("../utils")
sys.path.append("../data")

from Mpu6050 import Mpu6050
from Encoder import Encoder
from RPi_map import *
from constants import *
from calc_errores import calc_errores

class Motor():
    
    def __init__(self,giro,encoder):
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(CLKWA0, GPIO.OUT)
        GPIO.setup(CLKWA1, GPIO.OUT)
        GPIO.setup(CLKWB0, GPIO.OUT)
        GPIO.setup(CLKWB1, GPIO.OUT)
        
        #Sensores
        self.giro = giro
        self.encoder = encoder
        
        # Configura los pines GPIO como salidas PWM
        GPIO.setup(PWMA, GPIO.OUT)
        GPIO.setup(PWMB, GPIO.OUT)
        
        # Configura la frecuencia PWM (en Hz)
        pwm_frequency = 1000

        # Crea objetos PWM para los pines GPIO
        self.pwm_32 = GPIO.PWM(PWMA, pwm_frequency)
        self.pwm_33 = GPIO.PWM(PWMB, pwm_frequency)
    
        self.rotating = False
        self.moving = False
        self.rotacion = 0.0
        
        self.TIME_INT0    = 0.1
        self.time_thread = threading.Timer(self.TIME_INT0,self.timer_interrupt)
        self.time_thread.start()
    
    #Calibracion de las hot wheels
    def calibrate_wheels(self):
        print("Inicializando Robotito.\n")
        for i in range(5):
            self.avanzar(-60,-60);
            time.sleep(0.3)
            self.avanzar(60,60);
            time.sleep(0.3)    
        self.stop()
        time.sleep(0.3)
        print("Calibracion de ruedas terminada.\n")
    
    #Calibración de la MPU
    def calibrate_gyro(self):
        init_medValue = []
        meanError = 1
        error_target = 0.5
        while abs(meanError) > error_target:  
            self.giro.calibrate()
            meanError = 0
            for i in range(10):
                gyro_data = self.giro.get_gyro()
                meanError+= gyro_data[2]/10
                #init_medValue.append(gyro_data[2])
                time.sleep(0.005)
            #meanError = statistics.mean(init_medValue)
        print("MeanError -> ", meanError)
        print("Calibracion del giroscopo finalizada. \n")
    
    #Movimientos Simples
        #PWM1 es el motor de la izquierda    (Mirándolo desde el puente H)
        #PWM2 es el motor de la derecha
        #avanzar(self,izquierda, derecha)
    def avanzar(self,pwm1,pwm2):

        # Inicia el PWM con un ciclo de trabajo del pot% (máximo)
        self.pwm_32.start(abs(pwm1))
        self.pwm_33.start(abs(pwm2))
        self.moving = True

        if (pwm1 > 0):
            GPIO.output(CLKWA0,1)
            GPIO.output(CLKWA1,0)
        else:
            GPIO.output(CLKWA0,0)
            GPIO.output(CLKWA1,1)

        if (pwm2 > 0):
            GPIO.output(CLKWB0,1)
            GPIO.output(CLKWB1,0)
        else:
            GPIO.output(CLKWB0,0)
            GPIO.output(CLKWB1,1)

    #Detener los motores
    def stop(self):
        self.pwm_32.start(0)
        self.pwm_33.start(0)
        
        GPIO.output(CLKWA1,0)
        GPIO.output(CLKWA0,0)
        GPIO.output(CLKWB1,0)
        GPIO.output(CLKWB0,0)
        
        self.rotating = False
        self.moving = False
    
    #Controles
        #phi: grados
        #distancia: a recorrer
    def polar_control(self,phi1,distancia):
        self.stop()
        cant_pul = round((distancia*10)/theorical_move_per_pulse)
        self.rotate(phi1)
        while(self.rotating):
            pass
        self.encoder.iniciar_cuenta()
        self.avanzar(50,62)            
        while(((self.encoder.contador1+self.encoder.contador2)/2)<cant_pul):
            print(self.encoder.contador1, " ", self.encoder.contador2)
            print(cant_pul)
            pass
        self.stop()
        #time.sleep(pulsos/for_DutyCycle_50) #10 es para este ciclo de trabajo
        #self.stop()
        #return encoder.detener_cuenta()
        
    def linear_control_med(self,dist):
        
        vel = VEL_STANDARD
        out = []
        
        #Realizar la calibración de la MPU\
        gyro_tot = 0
        gyro_tot_array = []
        
        self.encoder.iniciar_cuenta()
        
    #Constantes
        tiempo = 0.1
        Kp1 = 0.08   #Constante proporcional
        Ki1 = 0.04 #Constante integral
        Kd1 = 0 #Constante derivativa
        Kp2 = 0.1   #Constante proporcional
        Ki2 = 0.04 #Constante integral
        Kd2 = 0 #Constante derivativa
        braking_range = 30 #mm
        
    #Condiciones iniciales
        array_vel_enc1 = []
        array_vel_enc2 = []
        contador = 1
        #Desplazamiento actual
        desp = 0 
        #Velocidades pasadas
        vel_enc1_ant = 0 
        vel_enc2_ant = 0
        #Errores proporcionales pasados
        err1_ant = 0
        err2_ant = 0
        #Errores integral pasados
        err1_i_ant = 0
        err2_i_ant = 0
        #Ciclos de trabajo
        dutyCycle = 70
        dutyCycle1 = dutyCycle
        dutyCycle2 = dutyCycle+10
        
        #Caso Base
        cnt1_ant = 0
        cnt2_ant = 0
        
        self.avanzar(dutyCycle1,dutyCycle2)

        while abs(desp) < (dist - braking_range):
            elem = []
            
            #Obtengo pulsos
            time.sleep(tiempo)
            contador1, contador2 = self.encoder.obtener_pulsos()
            
            # Obtener y corregir datos del giroscopio
            gyro_data = self.giro.get_gyro()
            #print("GiroData2 -> ", gyro_data[2])
            gyro_tot = gyro_tot + gyro_data[2]*tiempo
            gyro_tot_array.append(gyro_tot)
            print("Rotacion acumulada: ", round(gyro_tot,2))
            
            
            #Diferencias de Pulsos   
            diff_pulsos1 = contador1 - cnt1_ant  
            diff_pulsos2 = contador2 - cnt2_ant
            
    
            #Desplazamientos
            desp_enc1 = diff_pulsos1 * theorical_move_per_pulse
            desp_enc2 = diff_pulsos2 * theorical_move_per_pulse
            
            desp += (desp_enc1 + desp_enc2)/2
            
            #Velocidades
            vel_enc1 = desp_enc1/tiempo
            vel_enc2 = desp_enc2/tiempo
            
            array_vel_enc1.append(vel_enc1)
            array_vel_enc2.append(vel_enc2)
            
            elem.append(round(vel_enc1,2))
            elem.append(round(vel_enc2,2))
            
            #Calculo mediana cada 3 iteraciones
            if  contador % 3 == 0:
                
                mediana1 = statistics.median(array_vel_enc1)
                mediana2 = statistics.median(array_vel_enc2)
                array_vel_enc1 = []
                array_vel_enc2 = []
            
                vel_enc_med1 = mediana1
                vel_enc_med2 = mediana2
                
                #Errores Proporcionales
                err1 = vel + vel_enc_med1
                err2 = vel + vel_enc_med2

                #Errores Derivativos
                err1_d = (err1 - err1_ant)/tiempo
                err2_d = (err2 - err2_ant)/tiempo
                
                #Errores Integrales
                err1_i = err1_i_ant + (tiempo*err1)
                err2_i = err2_i_ant + (tiempo*err2)
                
                #PID
                pid1 = Kp1*err1 + Ki1*err1_i + Kd1*err1_d
                pid2 = Kp2*err2 + Ki2*err2_i + Kd2*err2_d
                
                dutyCycle1 += pid1
                dutyCycle2 += pid2
                
                if dutyCycle1 >=100:
                    dutyCycle1 = 100
                elif dutyCycle1 <= 0:
                    dutyCycle1 = 0
                if dutyCycle2 >=100:
                    dutyCycle2 = 100
                elif dutyCycle2 <= 0:
                    dutyCycle2 = 0    
                
                err1_ant = err1
                err2_ant = err2
                err1_i_ant = err1_i
                err2_i_ant = err2_i
                
                #Cargo una iteración en errores
                err_1_plot = vel + vel_enc1
                err_2_plot = vel + vel_enc2
                elem.append(round(err_1_plot,2))
                elem.append(round(err_2_plot,2))
                #print("Dut1:",dutyCycle1, "Dut2:",dutyCycle2)
                
                self.avanzar(dutyCycle1,dutyCycle2)
                
            #Actualización de valores
            vel_enc1_ant = vel_enc1
            vel_enc2_ant = vel_enc2
            cnt1_ant = contador1
            cnt2_ant = contador2
            contador+=1
            
            #Cargo salida
            out.append(elem)

        self.encoder.detener_cuenta()
        self.stop()
        
        return out
    
    def polarControl(self, phi_target, dist):
        superArrayReturn = []
        #Velocidad de Taget
    
        if phi_target == 0:
            k = 1.4
            alpha = 0.55
            dist_target = alpha * dist
        elif phi_target > 0:
            k = 0.7
            alpha = 0.6
            dist_target = (1 + 0.0025 * abs(phi_target)) * dist * alpha
            print("Dist_Target:", dist_target)
        else:
            if dist < 400:
                k = 1.1
            else:
                k = 0.95
            alpha = 0.6
            dist_target = (1 + 0.0025 * abs(phi_target)) * dist * alpha
            print("Dist_Target:", dist_target)
        
        #Velocidad
        arrayDutyCycle1 = []
        arrayDutyCycle2 = []
        dutyCycle = 50
        dutyCycle1 = dutyCycle
        dutyCycle2 = dutyCycle + 10
        
        #Giro
        gyro_array = []
        error_gyro_array = []
        gyro_tot = 0
        #Tiempo
        tiempo = 0.125
        
        #Desplazamiento
        current_desp = 0
        polar_coords = []
        desp_array = []
        error_desp_array = []
        error_desp_array.append(dist_target-current_desp)
        desp_array.append(current_desp)
        
        cnt1_ant = 0
        cnt2_ant = 0
        
        signed_phi = sign(phi_target)
        
        self.encoder.iniciar_cuenta()
        self.avanzar(dutyCycle1, dutyCycle2)
        
        if abs(phi_target) > 60 and abs(phi_target) < 120:
            self.rotate_with_timer(signed_phi*60)
            phi_target -= signed_phi*60
            time.sleep(2)
        if abs(phi_target) > 120:
            self.rotate_with_timer(signed_phi*120)
            phi_target -= signed_phi*120
            time.sleep(2)
        while abs(gyro_tot) <= -2+abs(phi_target) or abs(current_desp) < dist_target:
            gyro_data = self.giro.get_gyro()
            gyro_tot = gyro_tot + gyro_data[2]*tiempo
            gyro_array.append(gyro_tot)
            error_gyro_array.append(phi_target-gyro_tot)
            print("Rotacion acumulada: ", round(gyro_tot,2))
            
            diff_phase = phi_target - gyro_tot
            bias = k * diff_phase
            dutyCycle1 = dutyCycle - bias
            dutyCycle2 = dutyCycle + 10 + bias
            
            print("Dut1 ->", round(dutyCycle1,2))
            print("Dut2 ->", round(dutyCycle2,2))
            
            if dutyCycle1 >=100:
                dutyCycle1 = 100
            elif dutyCycle1 <= 0:
                dutyCycle1 = 10
            if dutyCycle2 >=100:
                dutyCycle2 = 100
            elif dutyCycle2 <= 0:
                dutyCycle2 = 10
                
            arrayDutyCycle1.append(dutyCycle1)
            arrayDutyCycle2.append(dutyCycle2)
        
            self.avanzar(dutyCycle1, dutyCycle2)
            
            contador1, contador2 = self.encoder.obtener_pulsos()
            
            #Diferencias de Pulsos   
            diff_pulsos1 = contador1 - cnt1_ant  
            diff_pulsos2 = contador2 - cnt2_ant
            
            #Desplazamientos
            desp_enc1 = diff_pulsos1 * theorical_move_per_pulse
            desp_enc2 = diff_pulsos2 * theorical_move_per_pulse

            #CALCULAR DIFERENCIAL DE DISTANCIAS
            current_desp += (desp_enc1 + desp_enc2)/2
            
            diff_desp = abs((desp_enc1 + desp_enc2)/(2*alpha))
            
            polar_coords.append((gyro_tot ,diff_desp))
            
            print("Desplazamiento actual -> ", round(abs(current_desp/alpha),2))
            desp_array.append(round(abs(current_desp/alpha),2))
            error_desp_array.append(dist_target-round(abs(current_desp/alpha),2))
            cnt1_ant = contador1
            cnt2_ant = contador2
            
            if abs(current_desp) >= 0.95 * dist_target:
                break
            
            time.sleep(tiempo)
            
        self.stop()
        self.giro.resetMPU()
        print("MPU Reseteada exitosamente")
        
        # Devolvemos todos los arrays para graficar
        #superArrayReturn.append(arrayDutyCycle1)
        #superArrayReturn.append(arrayDutyCycle2)
        #superArrayReturn.append(gyro_array)
        #superArrayReturn.append(error_gyro_array)
        #superArrayReturn.append(desp_array)
        #superArrayReturn.append(error_desp_array)
        #superArrayReturn.append(polar_coords)
        return polar_coords

    
    #Rotaciones
    def rotate(self, phi):
        self.giro.calibrate()
        error = calc_errores(self.giro)
        error_gyro = error[2]
        gyro_tot_mpu = 0
        
        target = abs(0.95*phi)
        
        tiempo = 0.1
        
        gyro_data = self.giro.get_gyro()
        
        while abs(gyro_data[2]) <= target:
            if phi < 0:
                self.avanzar(30,-30)
            else:
                self.avanzar(-30,30)
            time.sleep(tiempo)
            # Obtener y corregir datos del giroscopio
            gyro_data = self.giro.get_gyro()
            gyro_data[2] -= error_gyro[2]
    
            gyro_tot_mpu = gyro_tot_mpu + gyro_data[2]*0.1
            gyro_tot_mpu_array.append(gyro_tot_mpu)

            gyro_tot = gyro_tot_mpu
            gyro_tot_array.append(gyro_tot)
          
        self.stop()
        

    def rotate_with_timer(self, phi):
        self.rotacion_target = -phi
        self.rotacion = 0
        if ( (self.rotacion_target - self.rotacion) < 0 ):
            self.avanzar(50,-50)
        else:
            self.avanzar(-50,50)

        self.rotating = True
        
        
    def timer_interrupt(self):
        # Rotacion    
        velocidades = self.giro.get_gyro()
        #print("Giro Actual ->", velocidades[2])
        
        try:
            self.rotacion_target = self.rotacion_target * (-1)
        except:
            pass
        
        if (abs(velocidades[2]) > 0.1 ): # FIXME: Filtra el cambio de grados chicos, puede llevar a drifs #Umbral de error = 1
            self.rotacion += velocidades[2] * self.TIME_INT0 #* 1.15 #Intervalo de tiempo en cada interrupcion(delta t)

        if ( self.rotating == True ):
            if ( abs(self.rotacion - self.rotacion_target) <  18): #Umbral de error para acercarse al target: 18 grados
                self.stop()
                self.rotating = False

        '''if ( LOG_CONTROL == True ):
            self.log_control_file.write("%f %f %f %f %f %f %f %f %f\n"%(process_time(),self.distancia_target,self.distancia_tmp,self.rotacion,self.rotacion_target,gyro[2],self.vel_motor_A,self.vel_motor_B,self.moving))
        '''         
        self.time_thread.cancel()
        self.time_thread = threading.Timer(self.TIME_INT0,self.timer_interrupt)
        self.time_thread.start()
