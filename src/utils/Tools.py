import matplotlib.pyplot as plt
import numpy as np

def polarToCartesian(theta, dist):
    """Convierte coordenadas polares a cartesianas."""
    # Convertir ángulo a radianes respetando la convención dada
    theta = (theta*2*np.pi)/(360)
    print("Angulo-> ", theta)
    x = dist * np.sin(theta) * (-1)
    y = dist * np.cos(theta)
    print("x -> ", x)
    print("y -> ", y)
    return x, y

def drawArrowsFromOrigin(polar_coords, real_polarCoords):
    fig, ax = plt.subplots()
    max_range = max(abs(coord[1]) for coord in polar_coords)

    cartesian_coords = [polarToCartesian(theta,dist) for theta,dist in polar_coords]
    
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

    current_x, current_y = 0, 0  # Coordenadas iniciales en el origen
    for angle, distance in polar_coords:
        target_x = current_x + distance * np.sin(np.radians(angle)) * (-1)
        target_y = current_y + distance * np.cos(np.radians(angle))
        ax.arrow(current_x, current_y, target_x - current_x, target_y - current_y,
                 head_width=max_range * 0.05, head_length=max_range * 0.1,
                 fc='green', ec='green', length_includes_head=False)
        current_x, current_y = target_x, target_y  # Actualizar las coordenadas de inicio

    
    current_x, current_y = 0, 0
     
    for angle, distance in real_polarCoords:
        target_x = current_x + distance * np.sin(np.radians(angle)) * (-1)
        target_y = current_y + distance * np.cos(np.radians(angle))
        ax.arrow(current_x, current_y, target_x - current_x, target_y - current_y,
                 head_width=max_range * 0.05, head_length=max_range * 0.1,
                 fc='red', ec='red', length_includes_head=True)
        current_x, current_y = target_x, target_y  # Actualizar las coordenadas de inicio
        

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
        
    

#def graphRealTrayectory (superMegaArrayReturn, polar_coords):



