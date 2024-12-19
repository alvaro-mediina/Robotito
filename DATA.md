# **Proyecto Ingenia - Tercer Nivel**
Robotito

# Información importante

* Link del repo: [Link de GitHub](https://github.com/alvaro-mediina/Robotito)

## Tareas Pendientes
- [OK] Encoder.
- [OK] MPU.
- [OK] LiDAR.
- [OK] Hacer andar el motor.

## Conexiones

**Motor 1** 
PIN 32 -> Cable Negro-Morado -> GPIO 12 (PWM0)
PIN 15 -> Cable Amarillo -> GPIO 22
PIN 13 -> Cable Verde -> GPIO 27

**Motor 2**
PIN 33 -> Cable Blanco -> GPIO 13 (PWM1)
PIN 18 -> Cable Morado ->  GPIO 24
PIN 16 -> Cable Azul -> GPIO 23

**MPU**
PIN 4  -> Cable Rojo (5V)
PIN 25 -> Cable Marrón (GND)
PIN 5 -> Cable Negro (SCL)
PIN 3 -> Cable BLANCO (SDA)

**Puente H**
PIN 14 -> Cable Rosado (GND)


# Control PID

- La fase de target (a donde uno quiere llegar) debe ser convertida en una diferencia de ciclos de trabajo.
- Se debe ir monitoreando la fase porque cuando uno alcanzó la fase que quería, se anula la diferencia del ciclo de trabajo.
