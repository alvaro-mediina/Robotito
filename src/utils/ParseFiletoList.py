import sys
import matplotlib.pyplot as plt

sys.path.append("../utils")
sys.path.append("../data")
sys.path.append("../test")

def cleanFile(filename):
    with open(filename, 'w') as file:
        pass
    print("✅ Archivo Limpio ✅")

def parse_file_to_list_of_lists(filename):
    vel_enc1 = []
    vel_enc2 = []
    errors = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            elements = line.split('],') 
            for i, element in enumerate(elements):
                element = element.replace('[', '').replace(']', '').strip()  # Eliminar los corchetes
                values = [float(x) for x in element.split(',')] # Convertir los números a enteros
                vel_enc1.append(values[0])
                vel_enc2.append(values[1])
                
                if (i+1) % 3 == 0:
                    err1 = values[-2]
                    err2 = values[-1]
                    errors.append((err1,err2))
                    

    return vel_enc1, vel_enc2, errors

def plot_velocity_and_errors(vel_enc1, vel_enc2, err1_values, err2_values, error_indices):
    plt.figure(figsize=(10, 8))
    
    # Gráfico 1: Velocidades Encoder 2 IZQUIERDO y Error 2
    plt.subplot(2, 2, 1)
    plt.plot(vel_enc2, color='green', linewidth=4, label="Velocidad Encoder 2 IZQUIERDO", marker='o')
    plt.scatter(error_indices, err2_values, color='green', label="Error 2 (cada 3 iteraciones)", zorder=5)
    plt.title("Velocidad Encoder 2 (IZQUIERDO) y Error 2")
    plt.xlabel("Iteraciones")
    plt.ylabel("Velocidad / Error")
    plt.legend()

    # Gráfico 2: Velocidades Encoder 1 DERECHO y Error 1
    plt.subplot(2, 2, 2)
    plt.plot(vel_enc1, color='red', linewidth=4, label="Velocidad Encoder DERECHO", marker='o')
    plt.scatter(error_indices, err1_values, color='red', label="Error 1 (cada 3 iteraciones)", zorder=5)
    plt.title("Velocidad Encoder 1 (DERECHO) y Error 1")
    plt.xlabel("Iteraciones")
    plt.ylabel("Velocidad / Error")
    plt.legend()
    
    # Gráfico 3: Velocidades en comparacion
    plt.subplot(2 , 1, 2)
    plt.plot(vel_enc1, color='red', linewidth=4, label="Velocidad Encoder DERECHO", marker='o')
    plt.plot(vel_enc2, color='green', linewidth=4, label="Velocidad Encoder 2 IZQUIERDO", marker='o')
    plt.scatter(error_indices, err2_values, color='green', label="Error 2 (cada 3 iteraciones)", zorder=5)
    plt.scatter(error_indices, err1_values, color='red', label="Error 1 (cada 3 iteraciones)", zorder=5)
    
    plt.title("Comparacion de velocidades Encoder Derecho e Izquierdo y Errores")
    plt.xlabel("Iteraciones")
    plt.ylabel("Velocidad / Error")
    plt.legend()
    
    # Ajustar el layout para que los gráficos no se superpongan
    plt.tight_layout()
    plt.show()
    
    
    
    
