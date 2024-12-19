#Constantes
pulse_per_lap = 53
wheel_diameter = 60 #mm
theorical_move_per_pulse = 1.6 #mm
#theorical_move_per_pulse = 2.512 #mm

#Motor.py
VEL_STANDARD = 200
KP1 = 0.08   #Constante proporcional
KI1 = 0.04 #Constante integral
KD1 = 0 #Constante derivativa
KP2 = 0.1   #Constante proporcional
KI2 = 0.04 #Constante integral
KD2 = 0 #Constante derivativa
BRAKING_RANGE = 30 #mm

#MPU6050.py
FULL_SCALE_RANGE = 65.54

#Error de fase para el control de fase 0 (en grados)
PHASE_ERROR = 11.316 #°

