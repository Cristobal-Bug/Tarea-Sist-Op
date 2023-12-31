import pygame
import time
import threading
import sys

pygame.init()

matriz = []                                   #Creacion Matriz
for i in range(50):
    vector = []
    for j in range(30):
        vector.append('.')
    matriz.append(vector)

posibles_caminos = []                         # Vector para almacenar los posibles caminos
semaphore = threading.Semaphore()             # Semáforo para controlar el acceso al vector de caminos
semaphore_arriba = threading.Semaphore(0)     # Semáforo para el movimiento hacia arriba
semaphore_abajo = threading.Semaphore(0)      # Semáforo para el movimiento hacia abajo
semaphore_izquierda = threading.Semaphore(0)  # Semáforo para el movimiento hacia la izquierda
semaphore_derecha = threading.Semaphore(0)    # Semáforo para cel movimiento hacia la derecha

pantalla = pygame.display.set_mode((1920, 1080))

# Declaracion de los colores a utilizar en el laberinto

ColorNegro = (0, 0, 0)
ColorBlanco = (255, 255, 255)
ColorVerde = (0, 255, 0)
ColorAzul = (0, 0, 255)
ColorRojo = (255, 0, 0)
ColorPared = ColorBlanco

#Funcion para el movimiento hacia arriba

def arriba(x, y):
    global matriz, posibles_caminos
    i = y
    while (i >= 0) and (matriz[x][i] == '.'):
        matriz[x][i] = '-'
        time.sleep(0.5)
        pygame.draw.rect(pantalla, [255, 255, 255], ((x * 10 + 150, i * 10 + 150, 10, 10)))
        pygame.display.update()
        
        if (x > 0) and (matriz[x - 1][i] == '.'):
            with semaphore:
                posibles_caminos.append((x - 1, i, 'Izquierda'))

        if (x < 49) and (matriz[x + 1][i] == '.'):
            with semaphore:
                posibles_caminos.append((x + 1, i, 'Derecha'))
        i -= 1

    if i >= 0 and matriz[x][i] == 'V':
        print('Ventana encontrada en la matriz, posicion: (', x, ',', y, ')')
                                                 

#Funcion para el movimiento hacia abajo

def abajo(x, y):
    global matriz, posibles_caminos
    i = y
    while (i <= 29) and (matriz[x][i] == '.'):
        matriz[x][i] = '-'
        time.sleep(0.5)
        pygame.draw.rect(pantalla, [255, 255, 255], ((x * 10 + 150, i * 10 + 150, 10, 10)))
        pygame.display.update()
        
        if (x > 0) and (matriz[x - 1][i] == '.'):
            with semaphore:
                posibles_caminos.append((x - 1, i, 'Izquierda'))

        if (x < 49) and (matriz[x + 1][i] == '.'):
            with semaphore:
                posibles_caminos.append((x + 1, i, 'Derecha'))
        i += 1

    if i < 30 and matriz[x][i] == 'V':
        print('Ventana encontrada en la matriz, posicion: (', x, ',', y, ')')

#Funcion para el movimiento hacia la izquierda

def izquierda(x, y):
    global matriz, posibles_caminos
    i = x
    while (i >= 0) and (matriz[i][y] == '.'):
        matriz[i][y] = '-'
        time.sleep(0.5)
        pygame.draw.rect(pantalla, [255, 255, 255], ((i * 10 + 150, y * 10 + 150, 10, 10)))
        pygame.display.update()
        
        if (y > 0) and (matriz[i][y - 1] == '.'):
            with semaphore:
                posibles_caminos.append((i, y - 1, 'Arriba'))

        if (y < 29) and (matriz[i][y + 1] == '.'):
            with semaphore:
                posibles_caminos.append((i, y + 1, 'Abajo'))
        i -= 1

    if i >= 0 and matriz[i][y] == 'V':
        print('Ventana encontrada en la matriz, posicion: (', x, ',', y, ')')

#Funcion para el movimiento hacia la derecha

def derecha(x, y):
    global matriz, posibles_caminos
    i = x
    while (i <= 49) and (matriz[i][y] == '.'):
        matriz[i][y] = '-'
        time.sleep(0.5)
        pygame.draw.rect(pantalla, [255, 255, 255], ((i * 10 + 150, y * 10 + 150, 10, 10)))
        pygame.display.update()
        
        if (y > 0) and (matriz[i][y - 1] == '.'):
            with semaphore:
                posibles_caminos.append((i, y - 1, 'Arriba'))

        if (y < 29) and (matriz[i][y + 1] == '.'):
            with semaphore:
                posibles_caminos.append((i, y + 1, 'Abajo'))
        i += 1

    if i < 50 and matriz[i][y] == 'V':
        print('Ventana encontrada en la matriz, posicion: (', x, ',', y, ')')

pygame.draw.rect(pantalla,ColorAzul,( (150,150,500,300)))

#Agregar el archivo que contiene las paredes y la ventana dentro del laberinto

archivo = open("C:/Users/crist/Desktop/Tarea Sist Op/Laberinto.txt","r")
datos = archivo.readlines()
for dato in datos:
   posicion = dato.split(',')

   PosicionY = (int(posicion[0]))*10 + 150
   PosicionX = (int(posicion[1]))*10 + 150
 
   if (posicion[2] == "V\n"):
      pygame.draw.rect(pantalla,ColorVerde,( (PosicionX,PosicionY,10,10) ))
      matriz[int(posicion[1])][int(posicion[0])] = 'V'
   else:
      pygame.draw.rect(pantalla,ColorRojo,( (PosicionX,PosicionY,10,10) ))
      matriz[int(posicion[1])][int(posicion[0])] = 'X'

pygame.display.update()

#Inicializacion del movimiento dentro del laberinto

derecha(0,0)

#Funcion de la hebra dentro del laberinto
def hebra_laberinto():
    while True:
        with semaphore:
            if len(posibles_caminos) == 0:
                # No hay caminos disponibles, la hebra se bloquea
                time.sleep(0.1)
                continue
            x, y, direccion = posibles_caminos.pop()

        # Realiza la acción correspondiente en base a la dirección
        if direccion == 'Arriba':
            arriba(x, y)
        elif direccion == 'Abajo':
            abajo(x, y)
        elif direccion == 'Izquierda':
            izquierda(x, y)
        elif direccion == 'Derecha':
            derecha(x, y)

laberinto_thread = threading.Thread(target = hebra_laberinto)
laberinto_thread.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()




