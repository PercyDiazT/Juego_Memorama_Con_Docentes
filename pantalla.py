import pygame 
class Pantalla:
    def __init__(self,ancho,largo,titulo):
        """Inicializa el juego, la pantalla y el reloj de pygame."""
        pygame.init()  # Inicializa todos los módulos de pygame
        pygame.font.init()
        pygame.mixer.init()

        self.pantalla = pygame.display.set_mode((ancho,largo))  # Configura la dimension de la ventana
        pygame.display.set_caption(titulo)  # Configura el título de la ventana
        # self.reloj = pygame.time.Clock()  # Reloj para controlar los FPS
        color_blanco = (255, 255, 255)
        self.pantalla.fill(color_blanco)



    def mostrar_pantalla(self):
        pygame.display.flip()  # Actualiza el contenido de toda la pantalla
                    
    def cargar_arreglo_imagenes(self,arreglo):
        x = 0
        y = 0
        # Recorrer los cuadros
        for fila in arreglo:
            x = 0

            for cuadro in fila:
                """
                Si está descubierto o se debe mostrar, dibujamos la imagen real. Si no,
                dibujamos la imagen oculta
                """
                if cuadro.descubierto or cuadro.mostrar:
                    self.pantalla.blit(cuadro.imagen_real, (x, y))
                else:
                    pass
                    # Pantalla.blit(imagen_oculta, (x, y))
                x += cuadro.medida_cuadro
            y += cuadro.medida_cuadro

    def get_pantalla(self):
        """Retorna la pantalla actual de pygame."""
        return self.pantalla
    
    def actualizar(self):
        # Actualizamos la pantalla
        pygame.display.update() 
    
    #fonfo
    def fill(self,color):
        self.pantalla.fill(color)
    
    #blit
    def blit(self,imagen,coordenada):
        x,y =coordenada  
        self.pantalla.blit(imagen,(x,y))

        