import sys

if sys.version_info < (3, 10):
    sys.exit("Este juego requiere Python 3.10 o superior.")

import pygame

from assets import Recursos
from constants import (
    ALTO,
    ANCHO,
    DINERO_MAXIMO,
    DORADO,
    FONY,
    FPS,
    MENU_Y,
    NEGRO,
    OLEADAS,
    ROJO,
    STATS,
    VERDE,
)
from sprites import Aliado, Enemigo, Fuerte, MaCursor, SelectAliado


class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode([ANCHO, ALTO])
        self.reloj = pygame.time.Clock()
        self.recursos = Recursos()
        self.recursos.ost.play(-1)

        self.fonx = 0
        self.fony = FONY
        self.entuto = False
        self.oleadas = list(OLEADAS)
        self.spawn = 30
        self.generation = 15
        self.fin = False
        self.pausa = True
        self.findg = False
        self.findgd = False
        self.findgv = True
        self.reprod = False
        self.money = 0

        self.todos = pygame.sprite.Group()
        self.aliados = pygame.sprite.Group()
        self.sel_aliados = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.menu = pygame.sprite.Group()

        self.fuerte1 = Fuerte(self.recursos.fuerte1, x=0, y=170, vida=200)
        self.fuerte2 = Fuerte(self.recursos.fuerte2, x=1884, y=170, vida=200)
        self.todos.add(self.fuerte1, self.fuerte2)

        for i in range(5):
            selector = SelectAliado(i + 1)
            selector.rect.x = 81 * i + 150
            selector.rect.y = ALTO - 70
            selector.image = self.recursos.sprites_aliados[i][0][0]
            self.sel_aliados.add(selector)

        self.punt1 = MaCursor(self.recursos.cursor)
        self.punt1.rect.x = 8
        self.punt2 = MaCursor(self.recursos.cursor2)
        self.punt2.rect.x = 162
        self.menu.add(self.punt1, self.punt2)

    def run(self):
        while not self.fin:
            self._eventos()
            if not self.pausa:
                self._jugar()
            elif self.entuto:
                self._dibujar_tutorial()
            elif not self.findg:
                self._dibujar_menu()
            else:
                self._dibujar_fin()

    def reiniciar(self):
        for unidad in list(self.aliados) + list(self.enemigos):
            unidad.kill()
        self.fuerte1.vida = 500
        self.fuerte2.vida = 2000
        self.entuto = False
        self.oleadas = list(OLEADAS)
        self.spawn = 30
        self.generation = 15
        self.money = 0

    def _eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.fin = True
            elif event.type == pygame.KEYDOWN:
                self._tecla(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._click_aliado(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                for enemigo in self.enemigos:
                    enemigo.click = False
                for selector in self.sel_aliados:
                    selector.click = True

    def _tecla(self, tecla):
        if tecla == pygame.K_p:
            y = self.punt1.rect.y
            if y == MENU_Y["continuar"]:
                self.pausa = not self.pausa
            elif y == MENU_Y["salir"]:
                self.fin = True
            elif y == MENU_Y["tutorial"]:
                self.entuto = not self.entuto
            elif y == MENU_Y["reiniciar"]:
                self.reiniciar()
        elif tecla == pygame.K_UP:
            for cursor in self.menu:
                cursor.opu = True
        elif tecla == pygame.K_DOWN:
            for cursor in self.menu:
                cursor.opa = True

    def _click_aliado(self, pos):
        for selector in self.sel_aliados:
            idx = selector.id - 1
            if not selector.rect.collidepoint(pos):
                continue
            if not selector.click or self.money < STATS[2][idx]:
                continue

            selector.click = False
            aliado = Aliado(self.recursos.sprites_aliados[idx])
            aliado.damage = aliado.damage[idx]
            aliado.espera = aliado.espera[idx]
            aliado.vida = aliado.vida[idx]
            aliado.radius = aliado.radius[idx]
            aliado.precio = aliado.precio[idx]
            aliado.sonatk = self.recursos.sonidos_aliado_atk[idx]
            aliado.sonmuerte = self.recursos.sonidos_aliado_muerte[idx]
            self.money -= STATS[2][idx]
            if selector.id == 4:
                aliado.rect.y = ALTO - 210
            elif selector.id == 5:
                aliado.rect.y -= 10
            aliado.rect.x = self.fonx + 50
            self.aliados.add(aliado)
            self.todos.add(aliado)

    def _jugar(self):
        self._mover_camara()
        if self.money < DINERO_MAXIMO:
            self.money += 1

        self.pantalla.fill(NEGRO)
        self.pantalla.blit(self.recursos.fondo_mapa, [0, 0])
        self.pantalla.blit(self.recursos.fondo, [self.fonx, self.fony])

        self._generar_enemigo()
        self._combate()
        if self._ataque_fuerte(self.enemigos, self.fuerte1):
            self.findg = self.findgd = self.pausa = True
        if self._ataque_fuerte(self.aliados, self.fuerte2):
            self.findg = self.findgv = self.pausa = True
        self._eliminar_muertos()
        self._dibujar_hud()

        self.todos.update()
        self.todos.draw(self.pantalla)
        self.enemigos.draw(self.pantalla)
        self.aliados.draw(self.pantalla)
        self.sel_aliados.draw(self.pantalla)
        pygame.display.flip()
        self.reloj.tick(FPS)

    def _mover_camara(self):
        pos_x, _ = pygame.mouse.get_pos()
        ancho_mapa = self.recursos.mapa_rect.width
        if pos_x > ANCHO - 50 and self.fonx - 5 >= ANCHO - ancho_mapa:
            self.fonx -= 10
            for sprite in self.todos:
                sprite.rect.x -= 10
        if pos_x < 50 and self.fonx + 15 <= 0:
            self.fonx += 10
            for sprite in self.todos:
                sprite.rect.x += 10

    def _generar_enemigo(self):
        if self.generation:
            self.generation -= 1
            return
        if not self.oleadas:
            self.findgv = self.findg = self.pausa = True
            return

        tipo = self.oleadas.pop()
        self.generation = (tipo + 1) * self.spawn
        enemigo = Enemigo(self.recursos.sprites_enemigos[tipo])
        enemigo.id = tipo
        enemigo.radius = enemigo.radius[tipo]
        enemigo.damage = enemigo.damage[tipo]
        enemigo.espera = enemigo.espera[tipo]
        enemigo.vida = enemigo.vida[tipo]
        enemigo.sonatk = self.recursos.sonidos_enemigo_atk[tipo]
        enemigo.sonmuerte = self.recursos.sonidos_enemigo_muerte[tipo]
        enemigo.rect.x = self.recursos.mapa_rect.width + self.fonx - 100
        enemigo.rect.bottom = ALTO - 134
        self.enemigos.add(enemigo)
        self.todos.add(enemigo)

    def _puntos_vida(self, color, left, top, vida, paso):
        for i in range(vida):
            pygame.draw.circle(self.pantalla, color, [left + i * paso, top], 2)

    def _detener(self, unidad):
        unidad.vel_x = 0
        unidad.accion = 2 if unidad.attack else 0

    def _golpear(self, atacante, objetivo, sonido_despues=False):
        if atacante.espera[0] > 0:
            atacante.espera[0] -= 1
            return
        atacante.i = 0
        if sonido_despues:
            objetivo.vida -= atacante.damage
            atacante.sonatk.play()
        else:
            atacante.sonatk.play()
            objetivo.vida -= atacante.damage
        atacante.attack = True
        atacante.espera[0] = atacante.espera[1]

    def _combate(self):
        for enemigo in self.enemigos:
            for aliado in self.aliados:
                if aliado.vida > 0 and enemigo.vida > 0 and pygame.sprite.collide_circle(enemigo, aliado):
                    self._puntos_vida(ROJO, 5 + enemigo.rect.left, enemigo.rect.top - 5, enemigo.vida, 7)
                    self._detener(aliado)
                    self._golpear(aliado, enemigo, sonido_despues=True)

        for aliado in self.aliados:
            for enemigo in self.enemigos:
                if aliado.vida > 0 and enemigo.vida > 0 and pygame.sprite.collide_circle(aliado, enemigo):
                    self._puntos_vida(VERDE, 5 + aliado.rect.left, aliado.rect.top - 5, aliado.vida, 7)
                    self._detener(enemigo)
                    self._golpear(enemigo, aliado)

    def _ataque_fuerte(self, atacantes, fuerte):
        caido = False
        for unidad in atacantes:
            if fuerte.vida > 0 and unidad.vida > 0:
                if pygame.sprite.collide_circle(fuerte, unidad):
                    self._puntos_vida(ROJO, fuerte.rect.left, fuerte.rect.top - 5, fuerte.vida, 1)
                    self._detener(unidad)
                    self._golpear(unidad, fuerte)
            elif fuerte.vida <= 0:
                caido = True
        return caido

    def _eliminar_muertos(self):
        for aliado in self.aliados:
            for enemigo in self.enemigos:
                if enemigo.vida > 0 and aliado.vida > 0:
                    continue
                for otro in self.aliados:
                    otro.vel_x = 4
                    otro.accion = 1
                for otro in self.enemigos:
                    otro.vel_x = -4
                    otro.accion = 1
                if enemigo.vida <= 0:
                    enemigo.sonmuerte.play()
                    enemigo.kill()
                if aliado.vida <= 0:
                    aliado.sonmuerte.play()
                    aliado.kill()

    def _dibujar_hud(self):
        pygame.draw.polygon(
            self.pantalla,
            NEGRO,
            [(0, ALTO - 120), (0, ALTO), (ANCHO, ALTO), (ANCHO, ALTO - 120)],
        )
        self.pantalla.blit(self.recursos.txt_salud, [30, ALTO - 90])
        self.pantalla.blit(self.recursos.txt_golpe, [30, ALTO - 70])
        self.pantalla.blit(self.recursos.txt_costo, [30, ALTO - 50])
        self.pantalla.blit(self.recursos.money, [600, ALTO - 90])
        self.pantalla.blit(
            self.recursos.fuente.render(str(self.money), False, DORADO),
            [665, ALTO - 50],
        )
        for selector in self.sel_aliados:
            idx = selector.id - 1
            x, y = selector.rect.x + 15, selector.rect.y
            self.pantalla.blit(self.recursos.fuente2.render(str(STATS[0][idx]), False, ROJO), [x, y - 34])
            self.pantalla.blit(self.recursos.fuente2.render(str(STATS[1][idx]), False, VERDE), [x, y - 22])
            self.pantalla.blit(self.recursos.fuente2.render(str(STATS[2][idx]), False, DORADO), [x, y - 10])

    def _dibujar_tutorial(self):
        self.pantalla.fill(NEGRO)
        self.pantalla.blit(self.recursos.fondo_tutorial, [0, 0])
        self.punt1.rect.y = MENU_Y["tutorial"]
        pygame.display.flip()

    def _dibujar_menu(self):
        self.pantalla.fill(NEGRO)
        self.pantalla.blit(self.recursos.principal, [90, 27])
        self.pantalla.blit(self.recursos.continuar, [30, MENU_Y["continuar"]])
        self.pantalla.blit(self.recursos.reiniciar, [30, MENU_Y["reiniciar"]])
        self.pantalla.blit(self.recursos.tutorial, [30, MENU_Y["tutorial"]])
        self.pantalla.blit(self.recursos.salir, [30, MENU_Y["salir"]])
        self.menu.update()
        self.menu.draw(self.pantalla)
        pygame.display.flip()

    def _dibujar_fin(self):
        self.pantalla.fill(NEGRO)
        if self.findgd:
            self.recursos.ost.stop()
            self.pantalla.blit(self.recursos.gameover, [0, 0])
            sonido = self.recursos.ost_gameover
        else:
            self.pantalla.blit(self.recursos.victoria, [0, 0])
            sonido = self.recursos.ost_victoria
        pygame.display.flip()
        if not self.reprod:
            sonido.play()
            self.reprod = True


if __name__ == "__main__":
    Game().run()
