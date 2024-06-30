from pantalla import *
from cuadro import *

import pygame
import sys
import math
import time
import random
import pygame
pygame.init()
pygame.mixer.init()

cuadros = [
    [Cuadro("AngelMontesinos.png"), Cuadro("AngelMontesinos.png"),
     Cuadro("CarlosCorrales.png"), Cuadro("CarlosCorrales.png")],
    [Cuadro("GuillermoCalderon.png"), Cuadro("GuillermoCalderon.png"),
     Cuadro("KarimGuevara.png"), Cuadro("KarimGuevara.png")],
    [Cuadro("ManuelZuniga.png"), Cuadro("ManuelZuniga.png"),
     Cuadro("JoseEsquicha.png"), Cuadro("JoseEsquicha.png")],
    [Cuadro("KarinaRosas.png"), Cuadro("KarinaRosas.png"),
     Cuadro("JoseSulla.png"), Cuadro("JoseSulla.png")],
]

segundos_mostrar_pieza = 2  # Segundos para ocultar la pieza si no es la correcta
segundos_mostrar_pieza_inicio = 5  # Segundos para ocultar la pieza si no es la correcta
mostrar_temporalmente = False  # Nuevo indicador para mostrar los cuadros temporalmente


# Colores
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)

#Puntaje
puntos = 0
puntos_por_acierto = 100
puntos_por_error = -20

# Los sonidos
sonido_fondo = pygame.mixer.Sound("fondo.wav")
sonido_clic = pygame.mixer.Sound("clic.wav")
sonido_exito = pygame.mixer.Sound("ganador.wav")
sonido_fracaso = pygame.mixer.Sound("equivocado.wav")
sonido_voltear = pygame.mixer.Sound("voltear.wav")




medida_cuadro = cuadros[0][0].medida_cuadro
nombre_imagen_oculta = "oculta.png"
imagen_oculta_1 = pygame.image.load(nombre_imagen_oculta)
imagen_oculta = pygame.transform.scale(imagen_oculta_1, (medida_cuadro, medida_cuadro))



altura_boton = 30  # El botón de abajo, para iniciar juego
altura_banner = 30  # Altura del banner en píxeles

# Calculamos el tamaño de la pantalla en base al tamaño de los cuadrados
anchura_pantalla = len(cuadros[0]) * medida_cuadro
altura_pantalla = (len(cuadros) * medida_cuadro) + altura_boton + altura_banner
anchura_boton = anchura_pantalla


#CRONOMETRO
cronometro_activo = False
tiempo_inicio = 0
tiempo_restante = 1



pantalla_juego = Pantalla(anchura_pantalla,altura_pantalla,"MEMORAMA CON DOCENTES")

pantalla_juego.cargar_arreglo_imagenes(cuadros)
# pantalla.get_pantalla().fill(color_blanco)



pygame.mixer.Sound.play(sonido_fondo, -1)  # El -1 indica un loop infinito


# La fuente que estará sobre el botón
tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton)

# El botón, que al final es un rectángulo
boton = pygame.Rect(0, altura_pantalla - altura_boton,
                    anchura_boton, altura_pantalla)



ejecutando = True  # Estado del bucle del juego

# Banderas
# Bandera para saber si se debe ocultar la tarjeta dentro de N segundos
ultimos_segundos = None
puede_jugar = True  # Bandera para saber si reaccionar a los eventos del usuario
# Saber si el juego está iniciado; así sabemos si ocultar o mostrar piezas, además del botón
juego_iniciado = False
# Banderas de las tarjetas cuando se busca una pareja. Las necesitamos como índices para el arreglo de cuadros
# x1 con y1 sirven para la primer tarjeta
x1 = None
y1 = None
# Y las siguientes para la segunda tarjeta
x2 = None
y2 = None



# Ocultar todos los cuadros
def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False
def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True

# def reiniciar_juego():
#     global juego_iniciado
#     juego_iniciado = False

def reiniciar_juego():
    global juego_iniciado, cronometro_activo
    # Restablecer variables o reconfigurar el juego
    juego_iniciado = False
    cronometro_activo = False
    # tiempo_restante = 1  # Restablecer el tiempo como se requiera


def mostrar_todos_los_cuadros():
    """
    Esta función establece todos los cuadros del juego para que se muestren,
    ignorando si están descubiertos o no. Útil para una función de ayuda o depuración.
    """
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = True
            cuadro.descubierto = True  # Opcional, si también quieres marcarlos como descubiertos

# Ocultar todos los cuadros
def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False

def iniciar_juego():
    global juego_iniciado, mostrar_temporalmente,ultimos_segundos2, cronometro_activo, tiempo_inicio, puntos 
    puntos = 0
    ultimos_segundos2 = int(time.time())  # Guardamos el momento en que se mostraron
    mostrar_temporalmente = True  # Activamos el indicador de mostrar temporalmente

    # Aleatorizar 3 veces
    for i in range(3):
        aleatorizar_cuadros()

    mostrar_todos_los_cuadros()
    juego_iniciado = True

def aleatorizar_cuadros():
    # Elegir X e Y aleatorios, intercambiar
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal

def comprobar_si_gana():
    if gana():
        global cronometro_activo
        cronometro_activo = False  # Detener el cronómetro cuando el tiempo se agota
        pygame.mixer.Sound.play(sonido_exito)
        reiniciar_juego()
        #mostrar_ventana_ganaste()
        mostrar_ventana_ingreso_nombre(puntos, tiempo_restante, archivo='puntuaciones.txt')


# def mostrar_ventana_perdiste():
#     pygame.init()
#     ventana_perdiste = pygame.display.set_mode((300, 200))
#     pygame.display.set_caption("Perdiste")
#     fuente = pygame.font.SysFont("Arial", 24)
#     texto = fuente.render("¡Has perdido!", True, (255, 0, 0))
#     corriendo = True

#     while corriendo:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 ventana_perdiste = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
#                 corriendo = False
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     ventana_perdiste = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
#                     corriendo = False

#         ventana_perdiste.fill((0, 0, 0))  # Fondo negro
#         ventana_perdiste.blit(texto, (50, 75))  # Ajusta las coordenadas según necesites
#         pygame.display.flip()

#     # pygame.quit()
def mostrar_ventana_perdiste():
    global tiempo_restante
    pygame.init()
    ventana_perdiste = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Perdiste")
    fuente = pygame.font.SysFont("Arial", 24)
    texto = fuente.render("¡Has perdido!", True, (255, 0, 0))
    corriendo = True

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False  # Solo detener el bucle, no cambiar la configuración de la ventana aquí
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo = False  # Solo detener el bucle, no cambiar la configuración de la ventana aquí

        ventana_perdiste.fill((0, 0, 0))  # Fondo negro
        ventana_perdiste.blit(texto, (50, 75))  # Ajusta las coordenadas según necesites
        pygame.display.flip()

    # Aquí es donde deberías volver a la configuración de la ventana principal si es necesario
    pygame.display.set_mode((anchura_pantalla, altura_pantalla))
    tiempo_restante=1
    reiniciar_juego()


def mostrar_ventana_ganaste():
    pygame.init()
    ventana_ganaste = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Gasnaste")
    fuente = pygame.font.SysFont("Arial", 24)
    # texto = fuente.render("¡Ganaste", True, (255, 0, 0))
    texto_ganaste = fuente.render(f"¡Ganaste con {puntos} puntos!", True, (0, 255, 0))
    texto_tiempo = fuente.render(f"Tiempo restante: {int(tiempo_restante)}s", True, (0, 255, 0))

    corriendo = True

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.set_mode((anchura_pantalla, altura_pantalla))
                corriendo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo = False

        ventana_ganaste.fill((255, 255, 255))  # Fondo negro
        # ventana_ganaste.blit(texto, (50, 75))  # Ajusta las coordenadas según necesites
        ventana_ganaste.blit(texto_ganaste, (20, 50))  # Ajusta las coordenadas según necesites
        ventana_ganaste.blit(texto_tiempo, (20, 100))  # Ajusta las coordenadas según necesites
        pygame.display.flip()

def inicializar_puntuaciones(archivo='puntuaciones.txt'):
    try:
        with open(archivo, 'x') as f:
            f.write("")  # Crea un archivo vacío si no existe
    except FileExistsError:
        pass  # El archivo ya existe, no es necesario crearlo

def guardar_puntuacion(nombre, puntos, tiempo, archivo='puntuaciones.txt'):
    puntuaciones = cargar_puntuaciones(archivo)
    puntuaciones.append((nombre, puntos, tiempo))
    puntuaciones.sort(key=lambda x: (-x[1], - x[2]))  # Ordena por puntos descendente y tiempo ascendente
    puntuaciones = puntuaciones[:5]  # Conserva solo las mejores 5 puntuaciones

    with open(archivo, 'w') as f:
        for puntuacion in puntuaciones:
            f.write(f"{puntuacion[0]} {puntuacion[1]} {puntuacion[2]}\n")

def cargar_puntuaciones(archivo='puntuaciones.txt'):
    try:
        with open(archivo, 'r') as f:
            lineas = f.readlines()
        puntuaciones = [tuple(line.strip().split()) for line in lineas]
        return [(x[0], int(x[1]), float(x[2])) for x in puntuaciones]  # Convierte puntos y tiempo a tipos numéricos
    except FileNotFoundError:
        return []  # Si el archivo no existe, retorna una lista vacía


import pygame
import sys

def mostrar_puntuaciones(archivo='puntuaciones.txt'):
    pygame.init()
    ventana = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
    pygame.display.set_caption("MEMORAMA CON DONCENTES")
    fuente = pygame.font.SysFont("Arial", 24)
    texto = ''
    clock = pygame.time.Clock()
    # Carga de puntuaciones
    puntuaciones = cargar_puntuaciones(archivo)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Asegurarse de manejar el evento QUIT correctamente
                # iniciar_juego()
                # pygame.quit()
                # sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Solo detener el bucle, no cambiar la configuración de la ventana aquí

        ventana.fill((255, 255, 255))
        # Mostrar puntuaciones
        y_offset = 190  # Ajusta este valor según sea necesario
        for nombre, score, tiempo in puntuaciones:
            score_text = f"{nombre}: {score} puntos, {tiempo}s"
            score_surface = fuente.render(score_text, True, pygame.Color('black'))
            ventana.blit(score_surface, (20, y_offset))
            y_offset += 30  # Espacio entre líneas
        pygame.display.flip()
        clock.tick(30)
    pygame.display.set_mode((anchura_pantalla, altura_pantalla))



def mostrar_ventana_ingreso_nombre(puntos, tiempo_restante, archivo='puntuaciones.txt'):
    pygame.init()
    ventana = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
    pygame.display.set_caption("Ingresa tu nombre")
    fuente = pygame.font.SysFont("Arial", 24)
    input_box = pygame.Rect(20, 150, 200, 30)
    color_activo = pygame.Color('dodgerblue')
    color_inactivo = pygame.Color('lightskyblue')
    color = color_inactivo
    active = False
    texto = ''
    clock = pygame.time.Clock()
    texto_ganaste = fuente.render(f"¡Ganaste con {puntos} puntos!", True, (0, 255, 0))
    texto_tiempo = fuente.render(f"Tiempo restante: {int(tiempo_restante)}s", True, (0, 255, 0))
    # Carga de puntuaciones
    puntuaciones = cargar_puntuaciones(archivo)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.set_mode((anchura_pantalla, altura_pantalla))
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace clic en el input_box, activar el cuadro.
                pygame.display.set_mode((anchura_pantalla, altura_pantalla))

                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_activo if active else color_inactivo
            if event.type == pygame.KEYDOWN:
                pygame.display.set_mode((anchura_pantalla, altura_pantalla))

                if active:
                    if event.key == pygame.K_RETURN:
                        guardar_puntuacion(texto, puntos, tiempo_restante, archivo)
                        return  # Salir después de guardar
                    elif event.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        texto += event.unicode

        ventana.fill((255, 255, 255))
        # Renderizar el texto.
        txt_surface = fuente.render(texto, True, color)
        # Cambiar el tamaño de la caja si el texto es demasiado largo.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Dibujar el texto.
        ventana.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Dibujar el input box.
        pygame.draw.rect(ventana, color, input_box, 2)
        ventana.blit(texto_ganaste, (20, 50))  # Ajusta las coordenadas según necesites
        ventana.blit(texto_tiempo, (20, 100))  # Ajusta las coordenadas según necesites
        # Mostrar puntuaciones
        y_offset = 190  # Ajusta este valor según sea necesario
        for nombre, score, tiempo in puntuaciones:
            score_text = f"{nombre}: {score} puntos, {tiempo}s"
            score_surface = fuente.render(score_text, True, pygame.Color('black'))
            ventana.blit(score_surface, (20, y_offset))
            y_offset += 30  # Espacio entre líneas
        pygame.display.flip()
        clock.tick(30)


# Definir posición y tamaño del botón de puntuaciones
boton_puntuaciones = pygame.Rect(10, 10, 150, 30)

# Preparar el texto del botón de puntuaciones
texto_boton = fuente.render("Puntuaciones", True, color_blanco)
while True:
    # Escuchar eventos, pues estamos en un ciclo infinito que se repite varias veces por segundo
    for event in pygame.event.get():
        # Si quitan el juego, salimos
        if event.type == pygame.QUIT:
            sys.exit()
        # Si hicieron clic y el usuario puede jugar...
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

            

            """
            xAbsoluto e yAbsoluto son las coordenadas de la pantalla en donde se hizo
            clic. PyGame no ofrece detección de clic en imagen, por ejemplo. Así que
            se deben hacer ciertos trucos
            """
            # Si el click fue sobre el botón y el juego no se ha iniciado, entonces iniciamos el juego
            xAbsoluto, yAbsoluto = event.pos
            if boton_puntuaciones.collidepoint(event.pos):
                mostrar_puntuaciones()
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()

            else:
                # Si no hay juego iniciado, ignoramos el clic
                if not juego_iniciado:
                    continue
                """
                Ahora necesitamos a X e Y como índices del arreglo. Los índices no
                son lo mismo que los pixeles, pero sabemos que las imágenes están en un arreglo
                y por lo tanto podemos dividir las coordenadas entre la medida de cada cuadro, redondeando
                hacia abajo, para obtener el índice.
                Por ejemplo, si la medida del cuadro es 100, y el clic es en 140 entonces sabemos que le dieron
                a la segunda imagen porque 140 / 100 es 1.4 y redondeado hacia abajo es 1 (la segunda posición del
                arreglo) lo cual es correcto. Por poner otro ejemplo, si el clic fue en la X 50, al dividir da 0.5 y
                resulta en el índice 0
                """
                x = math.floor(xAbsoluto / medida_cuadro)
                y = math.floor((yAbsoluto-altura_banner) / medida_cuadro)
                # Primero lo primero. Si  ya está mostrada o descubierta, no hacemos nada
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierto:
                    # continue ignora lo de abajo y deja que el ciclo siga
                    continue
                # Si es la primera vez que tocan la imagen (es decir, no están buscando el par de otra, sino apenas
                # están descubriendo la primera)
                if x1 is None and y1 is None:
                    # Entonces la actual es en la que acaban de dar clic, la mostramos
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                else:
                    # En caso de que ya hubiera una clickeada anteriormente y estemos buscando el par, comparamos...
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                    # Si coinciden, entonces a ambas las ponemos en descubiertas:
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        cuadros[y1][x1].descubierto = True
                        cuadros[y2][x2].descubierto = True
                        puntos += puntos_por_acierto
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                        pygame.mixer.Sound.play(sonido_clic)
                    else:
                        pygame.mixer.Sound.play(sonido_fracaso)
                        puntos += puntos_por_error
                        # Si no coinciden, tenemos que ocultarlas en el plazo de [segundos_mostrar_pieza] segundo(s). Así que establecemos
                        # la bandera. Como esto es un ciclo infinito y asíncrono, podemos usar el tiempo para saber
                        # cuándo fue el tiempo en el que se empezó a ocultar
                        ultimos_segundos = int(time.time())
                        # Hasta que el tiempo se cumpla, el usuario no puede jugar
                        puede_jugar = False
                comprobar_si_gana()
                # if x == False:
                #     mostrar_ventana_perdiste()

            

    ahora = int(time.time())
    if mostrar_temporalmente and ahora - ultimos_segundos2 >= segundos_mostrar_pieza_inicio:  
        ocultar_todos_los_cuadros()  # Ocultamos todos los cuadros
        mostrar_temporalmente = False  # Desactivamos el indicador
        cronometro_activo = True
        tiempo_inicio = time.time() 
    # Y aquí usamos la bandera del tiempo, de nuevo. Si los segundos actuales menos los segundos
    # en los que se empezó el ocultamiento son mayores a los segundos en los que se muestra la pieza, entonces
    # se ocultan las dos tarjetas y se reinician las banderas
    if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        # En este momento el usuario ya puede hacer clic de nuevo pues las imágenes ya estarán ocultas
        puede_jugar = True

    # Hacer toda la pantalla blanca
    pantalla_juego.fill(color_blanco)

    # Dibuja el banner primero (si es solo un color sólido)
    pygame.draw.rect(pantalla_juego.get_pantalla(), color_azul, (0, 0, anchura_pantalla, altura_banner))
    # Banderas para saber en dónde dibujar las imágenes, pues al final
    # la pantalla de PyGame son solo un montón de pixeles
    x = 0
    y = altura_banner
    # Recorrer los cuadros
    for fila in cuadros:
        x = 0
        for cuadro in fila:
            """
            Si está descubierto o se debe mostrar, dibujamos la imagen real. Si no,
            dibujamos la imagen oculta
            """
            if cuadro.descubierto or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += medida_cuadro
        y += medida_cuadro

    # También dibujamos el botón
    if juego_iniciado:
        # Si está iniciado, entonces botón blanco con fuente gris para que parezca deshabilitado
        pygame.draw.rect(pantalla_juego.get_pantalla(), color_blanco, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_gris), (xFuente, yFuente))
    else:
        pygame.draw.rect(pantalla_juego.get_pantalla(), color_azul, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_blanco), (xFuente, yFuente))
    # Mostrar puntuación
    texto_puntuacion = fuente.render(f'Puntuación: {puntos}', True, color_negro)
    pantalla_juego.blit(texto_puntuacion, (10, altura_pantalla - altura_boton + 5))

        
    
    if cronometro_activo:
        tiempo_restante = 30 - (time.time() - tiempo_inicio)
    if tiempo_restante <= 0:
        tiempo_restante = 0
        cronometro_activo = False  # Detener el cronómetro cuando el tiempo se agota
        #sonido_fondo.stop()
        tiempo_restante = 1  # Restablecer el tiempo como se requiera
        mostrar_ventana_perdiste()

        


    texto_cronometro = fuente.render(f'Tiempo: {int(tiempo_restante)}s', True, color_negro)
    # Asegúrate de ajustar las coordenadas según tu diseño
    pantalla_juego.blit(texto_cronometro, (anchura_pantalla - 100, 5))

    # Dibujar el botón de puntuaciones en cada iteración
    pygame.draw.rect(pantalla_juego.get_pantalla(), color_azul, boton_puntuaciones)
    pantalla_juego.blit(texto_boton, (boton_puntuaciones.x + 5, boton_puntuaciones.y + 5))

    # Actualizamos la pantalla
    pygame.display.update()

