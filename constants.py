from pathlib import Path

ROOT = Path(__file__).resolve().parent

ANCHO = 800
ALTO = 480
FONY = 220
FPS = 15
DINERO_MAXIMO = 1000

VERDE = [0, 255, 0]
ROJO = [255, 0, 0]
NEGRO = [0, 0, 0]
DORADO = [255, 215, 0]

# salud, golpe, costo por aliado
STATS = [
    [5, 6, 4, 10, 15],
    [1, 2, 1, 5, 8],
    [18, 37, 56, 200, 250],
]

OLEADAS = [
    7, 1, 5, 4, 2, 3, 1, 0, 5, 2, 3, 4, 3, 2, 1, 3, 2, 1, 1, 0, 0,
    6, 1, 5, 4, 2, 3, 1, 0, 5, 2, 3, 4, 3, 2, 1, 3, 2, 1, 1, 0, 0,
]

MENU_Y = {
    "continuar": 90,
    "reiniciar": 130,
    "tutorial": 170,
    "salir": 210,
}
MENU_PASO = 40


def ruta(*partes):
    return str(ROOT.joinpath(*partes))
