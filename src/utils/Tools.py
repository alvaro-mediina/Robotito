import matplotlib.pyplot as plt
import numpy as np

def polar_to_cartesian(theta, dist):
    """Convierte coordenadas polares a cartesianas."""
    # Convertir ángulo a radianes respetando la convención dada
    theta = (theta*2*np.pi)/(360)
    print("Angulo-> ", theta)
    x = dist * np.sin(theta) * (-1)
    y = dist * np.cos(theta)
    print("x -> ", x)
    print("y -> ", y)
    return x, y

def drawArrowsFromOrigin(polar_coords):
    """Dibuja flechas secuenciales desde el origen a las coordenadas polares."""
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    
    #Convertir todas las coordenadas a cartesianas para calcular límites
    cartesian_coords = [polar_to_cartesian(theta,dist) for theta,dist in polar_coords]
    all_x = [x for x, y in cartesian_coords] + [0]
    all_y = [y for x, y in cartesian_coords] + [0]
    
    # Configurar límites dinámicamente
    max_range = max(max(map(abs, all_x)), max(map(abs, all_y))) * 2
    if max_range == 0:
        max_range = 1
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    
    # Dibujar el eje cartesiano
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
    
    # Inicializar punto de partida en el origen
    current_x, current_y = 0, 0
    
    for theta,dist in polar_coords:
        # Convertir a cartesianas
        target_x, target_y = polar_to_cartesian(theta,dist)

        # Dibujar flecha desde el punto actual al siguiente
        dx = target_x #- current_x
        dy = target_y #- current_y
        print("currentx -> ", current_x)
        print("currenty -> ", current_y)
        print("targetx -> ", target_x)
        print("targety -> ", target_y)
        if not (dx == 0 and dy == 0):
            ax.arrow(current_x,current_y,dx,dy,
                     head_width=max_range * 0.05, head_length=max_range * 0.1,
                     fc='blue', ec='blue', length_includes_head=True)

        # Actualizar el punto actual
        current_x = dx
        current_y = dy
    
    #Estilo y título
    ax.set_title('Flechas entre coordenadas polares')
    ax.set_aspect('equal')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
def drawAllData(superMegaArrayReturn,N):
    for i in range(N):
        plt.plot(superMegaArrayReturn[i][0], marker='o', linestyle='-', color='b')
        plt.xlabel('Iteraciones')
        plt.ylabel('Ciclo de Trabajo [%]')
        plt.title('Ciclo de trabajo para el motor 1')
        plt.show()
        plt.plot(superMegaArrayReturn[i][1], marker='o', linestyle='-', color='b')
        plt.xlabel('Iteraciones')
        plt.ylabel('Ciclo de Trabajo [%]')
        plt.title('Ciclo de trabajo para el motor 2')
        plt.show()
        plt.plot(superMegaArrayReturn[i][2], marker='o', linestyle='-', color='r')
        plt.xlabel('Iteraciones')
        plt.ylabel('Rotacion acumulada [°]')
        plt.title('Rotacion acumulada para el vehículo')
        plt.show()
        plt.plot(superMegaArrayReturn[i][3], marker='o', linestyle='-', color='r')
        plt.xlabel('Iteraciones')
        plt.ylabel('Error de rotacion [°]')
        plt.title('Error de rotación para el vehículo')
        plt.show()
        plt.plot(superMegaArrayReturn[i][4], marker='o', linestyle='-', color='g')
        plt.xlabel('Iteraciones')
        plt.ylabel('Desplazamiento acumulado [mm]')
        plt.title('Desplazamiento acumulado del vehículo')
        plt.show()
        plt.plot(superMegaArrayReturn[i][5], marker='o', linestyle='-', color='g')
        plt.xlabel('Iteraciones')
        plt.ylabel('Error de desplazamiento [mm]')
        plt.title('Error de desplazamiento del vehículo')
        plt.show()


