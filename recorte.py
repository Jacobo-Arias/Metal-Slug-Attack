def recorte(imagen, limites, ancho, alto=4):
    """Corta una hoja de sprites en filas según `limites`."""
    info = imagen.get_rect()
    an_img = info[2]
    al_img = info[3]
    # En Python 2 `/` entre enteros truncaba; pygame.subsurface exige enteros.
    al_corte = al_img // alto
    an_corte = an_img // ancho

    filas = []
    for k, cantidad in enumerate(limites):
        fila = []
        for i in range(cantidad):
            cuadro = imagen.subsurface(
                i * an_corte,
                k * al_corte,
                an_corte,
                al_corte,
            )
            fila.append(cuadro)
        filas.append(fila)
    return filas
