import pygame

from constants import DORADO, ROJO, VERDE, ruta
from recorte import recorte

HOJAS_ALIADOS = (
    (("Sprites", "marco.png"), [3, 8, 7, 2], 8, 4),
    (("Sprites", "ZombieTarma.png"), [12, 24, 12, 11], 24, 4),
    (("Sprites", "haduken.png"), [4, 13, 5, 7], 13, 4),
    (("Sprites", "tanque1.png"), [4, 14, 6, 4], 14, 4),
    (("Sprites", "MetalSlug.png"), [8, 21, 16], 21, 4),
)

HOJAS_ENEMIGOS = (
    (("Sprites", "arabe.png"), [4, 12, 8, 4], 12, 4),
    (("Sprites", "soldier.png"), [4, 12, 11], 12, 4),
    (("Sprites", "gunner.png"), [8, 16, 17, 4], 17, 4),
    (("Sprites", "ufo.png"), [8, 8, 8, 7], 8, 4),
    (("Sprites", "alien.png"), [16, 16, 17, 21], 21, 4),
    (("Sprites", "towertank.png"), [2, 6, 6, 6], 6, 4),
    (("Sprites", "cangrejo.png"), [7, 12, 12, 7], 12, 4),
    (("Sprites", "metalreal.png"), [5, 7, 31], 31, 4),
)

SONIDOS_ALIADO_ATK = (
    ("Sonidos", "marcoatk.ogg"),
    ("Sonidos", "zombiedisparo.ogg"),
    ("Sonidos", "ataqueprisionero.ogg"),
    ("Sonidos", "tanque1ataque.ogg"),
    ("Sonidos", "sfx_tanque.ogg"),
)

SONIDOS_ALIADO_MUERTE = (
    ("Sonidos", "muertemarco.ogg"),
    ("Sonidos", "muertezombie.ogg"),
    ("Sonidos", "muertearabe.ogg"),
    ("Sonidos", "tanque1muerte.ogg"),
    ("Sonidos", "tanquemuerte.ogg"),
)

SONIDOS_ENEMIGO_ATK = (
    ("Sonidos", "arabeatk.ogg"),
    ("Sonidos", "soldadoatk.ogg"),
    ("Sonidos", "ataquegunner.ogg"),
    ("Sonidos", "atqueufo.ogg"),
    ("Sonidos", "ataquealien.ogg"),
    ("Sonidos", "towertankatk.ogg"),
    ("Sonidos", "cangrejoatk.ogg"),
    ("Sonidos", "metalrealatk.ogg"),
)

SONIDOS_ENEMIGO_MUERTE = (
    ("Sonidos", "muertearabe.ogg"),
    ("Sonidos", "soldadomuerte.ogg"),
    ("Sonidos", "metralladoramuerte.ogg"),
    ("Sonidos", "muertealienyufo.ogg"),
    ("Sonidos", "muertealienyufo.ogg"),
    ("Sonidos", "towertankmuerte.ogg"),
    ("Sonidos", "cangrejomuerte.ogg"),
    ("Sonidos", "metalrealmuerte.ogg"),
)


def _imagen(*partes):
    return pygame.image.load(ruta(*partes))


def _sonido(*partes):
    return pygame.mixer.Sound(ruta(*partes))


def _hojas(definiciones):
    return [
        recorte(_imagen(*partes), limites, ancho, alto)
        for partes, limites, ancho, alto in definiciones
    ]


class Recursos:
    def __init__(self):
        self.fondo_tutorial = _imagen("Miscelanea", "fondotutorial.jpeg")
        self.fondo = _imagen("Miscelanea", "mapa.png")
        self.fondo_mapa = _imagen("Miscelanea", "fondomapa.png")
        self.gameover = _imagen("Miscelanea", "gameover.png")
        self.principal = _imagen("Miscelanea", "principal.png")
        self.continuar = _imagen("Miscelanea", "continuar.png")
        self.reiniciar = _imagen("Miscelanea", "reiniciar.png")
        self.tutorial = _imagen("Miscelanea", "tutorial.png")
        self.salir = _imagen("Miscelanea", "salir.png")
        self.cursor = _imagen("Miscelanea", "cursor.png")
        self.cursor2 = _imagen("Miscelanea", "cursor2.png")
        self.money = _imagen("Sprites", "Money.png")
        self.fuerte1 = _imagen("Sprites", "Fuerte1.png")
        self.fuerte2 = _imagen("Sprites", "Fuerte2.png")
        self.victoria = _imagen("Miscelanea", "fotovictoria.jpeg")

        self.ost = _sonido("Sonidos", "ost.ogg")
        self.ost_gameover = _sonido("Sonidos", "GameOver.ogg")
        self.ost_victoria = _sonido("Sonidos", "Victoria.ogg")

        self.sprites_aliados = _hojas(HOJAS_ALIADOS)
        self.sprites_enemigos = _hojas(HOJAS_ENEMIGOS)
        self.sonidos_aliado_atk = [_sonido(*p) for p in SONIDOS_ALIADO_ATK]
        self.sonidos_aliado_muerte = [_sonido(*p) for p in SONIDOS_ALIADO_MUERTE]
        self.sonidos_enemigo_atk = [_sonido(*p) for p in SONIDOS_ENEMIGO_ATK]
        self.sonidos_enemigo_muerte = [_sonido(*p) for p in SONIDOS_ENEMIGO_MUERTE]

        self.fuente = pygame.font.Font(None, 30)
        self.fuente2 = pygame.font.Font(None, 20)
        self.txt_salud = self.fuente.render("Salud", False, ROJO)
        self.txt_golpe = self.fuente.render("Golpe", False, VERDE)
        self.txt_costo = self.fuente.render("Costo", False, DORADO)
        self.mapa_rect = self.fondo.get_rect()
