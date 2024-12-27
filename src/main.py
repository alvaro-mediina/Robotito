import numpy as np
import matplotlib.pyplot as plt

def polarToCartesian(current_x,  current_y, phi, dist):
    target_x = current_x + dist * np.sin(np.radians(phi)) * (-1)
    target_y = current_y + dist * np.cos(np.radians(phi))
    return target_x, target_y

def drawArrowsFromOrigin(polar_coords, real_polarCoords):
    fig, ax = plt.subplots()
    
    max_range = 1000

    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    
    # Dibujar el eje cartesiano
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')

    current_x, current_y = 0, 0  # Coordenadas iniciales en el origen
    for angle, dist in polar_coords:
        target_x, target_y = polarToCartesian(current_x, current_y, angle, dist) 
        ax.arrow(current_x, current_y, target_x - current_x, target_y - current_y,
                 head_width=max_range * 0.03, head_length=max_range * 0.1,
                 fc='green', ec='green', length_includes_head=False)
        current_x, current_y = target_x, target_y  # Actualizar las coordenadas de inicio

    
    current_x, current_y = 0, 0
     
    for angle, dist in real_polarCoords:
        target_x = current_x + dist * np.sin(np.radians(angle)) * (-1)
        target_y = current_y + dist * np.cos(np.radians(angle))
        ax.arrow(current_x, current_y, target_x - current_x, target_y - current_y,
                 head_width=max_range * 0.03, head_length=max_range * 0.05,
                 fc='red', ec='red', length_includes_head=True)
        current_x, current_y = target_x, target_y  # Actualizar las coordenadas de inicio
        

    ax.set_title('Flechas entre coordenadas polares')
    ax.set_aspect('equal')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


polar_coords = [(0,500)]
real_polarCoords = [
    (-0.00999389685688129, 0.0),
    (0.2660970399755874, 7.2727272727272725),
    (0.6795086969789441, 11.636363636363637),
    (1.7070491303021054, 13.09090909090909),
    (1.9564388159902348, 16.0),
    (1.5859780286847727, 14.545454545454545),
    (1.4825297528227037, 18.909090909090907),
    (0.7802105584375955, 21.818181818181817),
    (-0.5610314311870611, 21.818181818181817),
    (-0.527158986878242, 20.363636363636363),
    (-0.37694537686908736, 24.727272727272727),
    (-1.1097802868477262, 20.363636363636363),
    (-0.9042569423252972, 23.272727272727273),
    (-1.4749771132133045, 26.18181818181818),
    (-2.2001830942935605, 24.727272727272727),
    (-3.585291425083917, 23.272727272727273),
    (-3.036466280134268, 17.454545454545457),
    (-3.5175465364662792, 23.272727272727273),
    (-0.647619774183704, 24.727272727272727),
    (-0.9780286847726573, 26.18181818181818),
    (0.5186908758010379, 26.18181818181818),
    (1.857110161733293, 24.727272727272727),
    (1.303555080866647, 24.727272727272727),
    (0.6718034787915784, 26.18181818181818),
    (0.42531278608483447, 21.818181818181817),
    (0.5583613060726282, 24.727272727272727),
]


drawArrowsFromOrigin(polar_coords, polar_coords)