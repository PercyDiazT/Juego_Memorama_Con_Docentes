import pygame
class Cuadro:
    def __init__(self, fuente_imagen, medida_cuadro = 140):
        self.mostrar = True
        self.descubierto = False
        self.medida_cuadro = medida_cuadro
        """
        Una cosa es la fuente de la imagen (es decir, el nombre del archivo) y otra
        la imagen lista para ser pintada por PyGame
        La fuente la necesitamos para más tarde, comparar las tarjetas
        """
        self.fuente_imagen = fuente_imagen
        imagen_cargada = pygame.image.load(fuente_imagen)
        # Redimensionar la imagen al tamaño deseado
        self.imagen_real = pygame.transform.scale(imagen_cargada, (medida_cuadro, medida_cuadro))
 