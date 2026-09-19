import pygame

from constants import ALTO, MENU_PASO, MENU_Y, STATS


class UnidadAnimada(pygame.sprite.Sprite):
    """Unidad con hoja de sprites, animación y desplazamiento horizontal."""

    def __init__(self, filas, vel_x):
        super().__init__()
        self.filas = filas
        self.accion = 1
        self.i = 0
        self.f = self.filas[self.accion]
        self.image = self.f[self.i]
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = ALTO - 190
        self.vel_x = vel_x
        self.attack = False
        self.sonatk = None
        self.sonmuerte = None

    def update(self):
        self.rect.x += self.vel_x
        self.f = self.filas[self.accion]
        self.i += 1
        if self.i >= len(self.f):
            self.i = 0
            self.attack = False
        self.image = self.f[self.i]


class Enemigo(UnidadAnimada):
    def __init__(self, filas):
        super().__init__(filas, vel_x=-4)
        self.id = 0
        self.vida = [5, 6, 7, 4, 5, 8, 50, 100]
        self.radius = [40, 70, 80, 30, 50, 50, 30, 60]
        self.damage = [1, 2, 1, 3, 3, 5, 10, 15]
        self.espera = [
            [0, 30], [0, 30], [0, 15], [0, 20],
            [0, 25], [0, 30], [0, 45], [0, 45],
        ]


class Aliado(UnidadAnimada):
    def __init__(self, filas):
        super().__init__(filas, vel_x=4)
        self.precio = STATS[2]
        self.vida = [5, 6, 4, 10, 20]
        self.radius = [40, 50, 50, 20, 40]
        self.damage = [1, 2, 1, 5, 8]
        self.espera = [
            [0, 30], [0, 30], [0, 15], [0, 30], [0, 45],
        ]


class SelectAliado(pygame.sprite.Sprite):
    def __init__(self, unidad_id):
        super().__init__()
        self.image = pygame.Surface([40, 80])
        self.id = unidad_id
        self.click = True
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = ALTO - 100


class Fuerte(pygame.sprite.Sprite):
    def __init__(self, imagen, x=0, y=170, vida=200):
        super().__init__()
        self.image = imagen
        self.vida = vida
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MaCursor(pygame.sprite.Sprite):
    def __init__(self, imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = 226
        self.rect.y = MENU_Y["continuar"]
        self.opu = False
        self.opa = False

    def update(self):
        if self.opu:
            self.rect.y = MENU_Y["salir"] if self.rect.y == MENU_Y["continuar"] else self.rect.y - MENU_PASO
            self.opu = False
        elif self.opa:
            self.rect.y = MENU_Y["continuar"] if self.rect.y == MENU_Y["salir"] else self.rect.y + MENU_PASO
            self.opa = False
