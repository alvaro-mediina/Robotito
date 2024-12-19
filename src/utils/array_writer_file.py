import os

def write(nombre_archivo, datos):
    # Comprobamos si el archivo existe
    if not os.path.exists(nombre_archivo):
        print(f"El archivo {nombre_archivo} no existe, se va a crear.")
    else:
        print(f"El archivo {nombre_archivo} ya existe, se modificará.")
    
    
    with open('nombre_del_archivo.txt', 'w') as file:
        pass  # Al abrir el archivo en modo 'w', se vacía automáticamente.

    # Convertimos los datos (arreglo) a una cadena de texto, por ejemplo separada por comas
    datos_str = ", ".join(map(str, datos))
    

    # Abrimos el archivo en modo 'a' (append) para escribir al final sin sobrescribir
    with open(nombre_archivo, 'a') as archivo:
        archivo.write(datos_str)
        archivo.write("\n")
        print(f"Datos escritos en {nombre_archivo} con éxito.")