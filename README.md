# Metal Slug Attack

Juego de oleadas inspirado en *Metal Slug Attack*. Defiendes tu fuerte, gastas dinero para desplegar aliados y aguantas hasta que se acaben los enemigos.

Proyecto de Computación Gráfica, migrado a **Python 3.10+** (probado en 3.12).

## Requisitos

- Python 3.10 o superior
- [pygame-ce](https://pypi.org/project/pygame-ce/) 2.5.8 o mayor

En Windows, si `python` apunta a 3.9, usa el launcher `py`:

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 PruebaGenInf.py
```

En otros sistemas:

```bash
python3 -m pip install -r requirements.txt
python3 PruebaGenInf.py
```

## Controles

### Menú

| Tecla | Acción |
| --- | --- |
| Flecha arriba / abajo | Mover el cursor |
| **P** | Confirmar la opción |

Opciones: Continuar, Reiniciar, Tutorial y Salir.

### Partida

| Control | Acción |
| --- | --- |
| Clic en un aliado de la barra inferior | Desplegarlo si alcanza el dinero |
| Mouse a los bordes izquierdo/derecho | Desplazar la cámara |
| **P** (con Continuar seleccionado) | Pausar y volver al menú |

El dinero sube solo hasta 1000. Cada unidad muestra salud, golpe y costo en el HUD.

## Estructura

| Archivo | Rol |
| --- | --- |
| `PruebaGenInf.py` | Punto de entrada y bucle del juego |
| `sprites.py` | Aliados, enemigos, fuertes y cursor |
| `assets.py` | Carga de imágenes y sonidos |
| `constants.py` | Resolución, colores, stats y oleadas |
| `recorte.py` | Corte de hojas de sprites |

Los recursos están en `Sprites/`, `Sonidos/` y `Miscelanea/`.
