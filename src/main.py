import matplotlib
matplotlib.use('TkAgg')
import math
import numpy as np
import matplotlib.pyplot as plt

def polarToCartesian(current_x,  current_y, phi, dist):
    target_x = current_x + dist * np.sin(np.radians(phi)) * (-1)
    target_y = current_y + dist * np.cos(np.radians(phi))
    return target_x, target_y

def drawPointsFromOrigin(polar_coords, real_polarCoords):
    fig, ax = plt.subplots()
    
    max_range = 1000

    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    
    # Dibujar el eje cartesiano
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
    arrayErrorIdeal = []
    current_x, current_y = 0, 0  # Coordenadas iniciales en el origen
    for angle, dist in polar_coords:
        target_x, target_y = polarToCartesian(current_x, current_y, angle, dist)
        arrayErrorIdeal.append((target_x,target_y))
        ax.plot(target_x, target_y, 'go')  # 'go' para puntos verdes
        current_x, current_y = target_x, target_y  # Actualizar las coordenadas de inicio

    current_x, current_y = 0, 0
    arrayErrorReal = []
    i = 0
    for angle, dist in real_polarCoords:
        target_x = current_x + dist * np.sin(np.radians(angle)) * (-1)
        target_y = current_y + dist * np.cos(np.radians(angle))
        if i == 27 or i == 61 or i == len(real_polarCoords)-1:
            arrayErrorReal.append((target_x,target_y))
        ax.plot(target_x, target_y, 'ro')  # 'ro' para puntos rojos
        current_x, current_y = target_x, target_y  # Actualizar las coordenadas de inicio
        i += 1
    # Configurar los límites y mostrar la gráfica
    ax.set_aspect('equal', 'box')
    ax.plot([], [], 'go', label='Ideal') 
    ax.plot([], [], 'ro', label='Real')  
    ax.legend(loc='upper right')  # Mostrar la leyenda
    plt.title("Trayectoria Ideal vs Trayectoria Real")
    plt.show()
    return arrayErrorIdeal, arrayErrorReal
    
def calculateMeanError(arrayErrorIdeal, arrayErrorReal):
    coordsError = []
    for i in range(len(arrayErrorIdeal)):
        idealCoord = arrayErrorIdeal[i]
        realCoord = arrayErrorReal[i]
        
        # Restar las coordenadas componente por componente
        error = (realCoord[0] - idealCoord[0], realCoord[1] - idealCoord[1])
        coordsError.append(error)
    
    arrayDistances = []
    for coord in coordsError:
        arrayDistances.append(math.sqrt(coord[0]**2 + coord[1]**2))

    print("El error promedio es -> ", np.mean(arrayDistances), " mm")

polar_coords = [(0,550), (90, 550), (180,550)]

realPolarCoords = [
    (-0.03322398535245652, 0.0),
    (0.19102837961550195, 7.2727272727272725),
    (0.6212618248397924, 13.09090909090909),
    (0.7482453463533719, 16.0),
    (-0.18709948123283493, 20.363636363636363),
    (1.339792493133964, 18.90909090909091),
    (1.400022886786695, 17.454545454545457),
    (1.519377479401892, 21.818181818181817),
    (1.459452242905096, 20.363636363636363),
    (0.5813243820567593, 21.818181818181817),
    (0.7197512969179127, 26.18181818181818),
    (0.7113213304851999, 20.36363636363636),
    (2.467081171803479, 26.18181818181818),
    (2.2793713762587733, 26.18181818181818),
    (3.9378623741226733, 26.18181818181818),
    (4.011443393347574, 26.18181818181818),
    (2.872024717729631, 21.818181818181817),
    (3.973603906011596, 18.90909090909091),
    (4.01476197741837, 26.18181818181818),
    (5.364281354897772, 24.727272727272727),
    (4.753166005492828, 23.272727272727273),
    (6.028303326212999, 26.18181818181818),
    (4.902235276167225, 24.727272727272727),
    (6.156393042416844, 26.18181818181818),
    (5.776052792187976, 21.818181818181817),
    (5.428135489777234, 26.18181818181818),
    (0.027807445834604816, 17.333333333333343),
    (1.1484589563625267, 5.333333333333334),
    (3.4477799816905703, 12.000000000000002),
    (5.319880988709185, 16.000000000000004),
    (6.608368935001526, 17.333333333333336),
    (7.641287763198047, 16.000000000000004),
    (9.131942325297528, 20.0),
    (7.7522123893805315, 16.000000000000004),
    (9.218072932560268, 22.66666666666667),
    (9.940112908147697, 21.333333333333336),
    (12.031545620994812, 21.333333333333336),
    (13.501220628623742, 22.66666666666667),
    (14.75537839487336, 17.33333333333334),
    (14.863289594140982, 18.666666666666668),
    (17.101579188281963, 24.0),
    (17.121757705218187, 21.333333333333336),
    (18.951899603295697, 18.666666666666668),
    (19.61481537992066, 20.0),
    (20.418866341165703, 10.666666666666668),
    (19.721925541653956, 18.666666666666668),
    (20.665204455294482, 22.66666666666667),
    (19.708880073237722, 24.0),
    (20.94205828501679, 24.0),
    (19.678669514800127, 21.333333333333336),
    (21.316180958193474, 22.66666666666667),
    (21.7750228867867, 21.333333333333336),
    (22.592424473603913, 21.333333333333336),
    (22.578272810497413, 21.333333333333336),
    (24.488518462007942, 17.33333333333334),
    (23.970857491608186, 22.66666666666667),
    (23.930004577357348, 20.0),
    (24.74168446750077, 22.66666666666667),
    (24.916348794629243, 22.66666666666667),
    (24.503585596582248, 21.333333333333336),
    (24.041234360695768, 22.66666666666667),
    (0.0030134269148611448, 14.666666666666668),
    (1.4936679890143423, 4.000000000000001),
    (3.2627784559047908, 9.333333333333334),
    (4.757247482453463, 13.333333333333334),
    (6.522543484894721, 16.000000000000004),
    (8.40608788526091, 18.666666666666668),
    (10.54901586817211, 18.666666666666668),
    (11.36641745498932, 18.666666666666668),
    (13.234703997558743, 22.66666666666667),
    (13.790814769606348, 21.333333333333336),
    (16.246528837351235, 20.0),
    (17.403417760146475, 21.333333333333336),
    (18.182674702471772, 17.33333333333334),
    (19.391058895331096, 24.0),
    (21.350892584681112, 18.666666666666668),
    (21.63236191638694, 24.0),
    (23.172604516325908, 24.0),
    (22.685459261519682, 21.333333333333336),
    (24.39353829722307, 20.0),
    (25.04310344827586, 21.333333333333336),
    (26.665357033872443, 18.666666666666668),
    (26.6702776930119, 18.666666666666668),
    (24.479974061641744, 18.666666666666668),
    (25.177220018309427, 21.333333333333336),
    (25.357606042111684, 20.0),
    (27.248779371376255, 24.0),
    (26.841737870003048, 22.66666666666667),
    (27.701098565761363, 22.66666666666667),
    (27.650709490387545, 21.333333333333336),
    (27.503051571559347, 22.66666666666667),
    (27.160855965822392, 18.666666666666668),
    (26.652731156545617, 22.66666666666667),
    (28.408490997863897, 17.333333333333336),
    (28.527845590479092, 20.0),
    (26.65223527616722, 21.333333333333336)
]

# Modificación de las coordenadas
for i in range(27, 61):
    realPolarCoords[i] = (realPolarCoords[i][0] + 65, realPolarCoords[i][1])

for i in range(61, len(realPolarCoords)):
    realPolarCoords[i] = (realPolarCoords[i][0] + 160, realPolarCoords[i][1])

# Cálculo del error:



# Mostrar el arreglo modificado
for coord in realPolarCoords:
    print(coord)

arrayErrorIdeal = []
arrayErrorReal = []

arrayErrorIdeal, arrayErrorReal = drawPointsFromOrigin(polar_coords, realPolarCoords)

calculateMeanError(arrayErrorIdeal, arrayErrorReal)