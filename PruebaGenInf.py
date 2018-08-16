import pygame
import random
import recorte
Ancho=800
Alto=480
VERDE=[0,255,0]
AZUL=[0,0,255]
ROJO=[255,0,0]
NEGRO=[0,0,0]
BLANCO=[255,255,255]
DORADO=[255,215,0]
fonx=0
fony=220

stats=[[5,6,4,10,15],[1,2,1,5,8],[18,37,56,200,250]]


class MaCursor(pygame.sprite.Sprite):
    def __init__(self,pont):
        pygame.sprite.Sprite.__init__(self)
        self.image=pont
        self.rect=self.image.get_rect()
        self.rect.x=226
        self.rect.y=90
        self.opu=False
        self.opa=False

    def update(self):
        if self.opu:
             if self.rect.y==90:
                 self.rect.y=210
                 self.opu=False
             else:
                 self.rect.y-=40
                 self.opu=False
        elif self.opa:
            if self.rect.y==210:
                self.rect.y=90
                self.opa=False
            else:
                self.rect.y+=40
                self.opa=False

class Enemigo (pygame.sprite.Sprite):
    def __init__(self,filas):
        pygame.sprite.Sprite.__init__(self)
        self.filas = filas
        self.id = 0
        self.accion = 1
        self.i = 0
        self.f = self.filas[self.accion]
        self.image = self.f[self.i]
        self.rect = self.image.get_rect()
        self.vida=[5,6,7,4,5,8,50,100]
        self.rect.x,self.rect.y = 10,Alto-190
        self.vel_x = -4
        self.radius = [40,70,80,30,50,50,30,60]
        self.damage=[1,2,1,3,3,5,10,15]
        self.espera=[[0,30],[0,30],[0,15],[0,20],[0,25],[0,30],[0,45],[0,45]]
        self.attack = False
        self.sonatk = None
        self.sonmuerte = None

    def update (self):
        self.rect.x+= self.vel_x
        self.f = self.filas[self.accion]
        self.i += 1
        if self.i >= len(self.f):
            self.i = 0
            self.attack = False
        self.image = self.f[self.i]


class Aliado (pygame.sprite.Sprite):
    def __init__(self,filas):
        pygame.sprite.Sprite.__init__(self)
        self.filas = filas
        self.accion = 1
        self.i = 0
        self.precio = stats[2]
        self.f = self.filas[self.accion]
        self.image = self.f[self.i]
        self.rect = self.image.get_rect()
        self.vida=[5,6,4,10,20]
        self.rect.x,self.rect.y = 10,Alto-190
        self.vel_x = 4
        self.sonatk = None
        self.sonmuerte = None
        self.radius = [40,50,50,20,40]
        self.damage=[1,2,1,5,8]
        self.espera=[[0,30],[0,30],[0,15],[0,30],[0,45]]
        self.attack = False

    def update (self):
        self.rect.x+= self.vel_x
        self.f = self.filas[self.accion]
        self.i += 1
        if self.i >= len(self.f):
            self.i = 0
            self.attack = False
        self.image = self.f[self.i]

class SelectAliado (pygame.sprite.Sprite):
    def __init__(self,id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40,80])
        self.id = id
        self.click = True
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = 5,Alto-100

class fuerte(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/Fuerte1.png")
        self.vida = 200
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = 0,170

if __name__ == '__main__':
    pygame.init()
    pantalla=pygame.display.set_mode([Ancho,Alto])
    pygame.display.flip()

    '''--------------------------globales---------------------------------'''
    entuto = False
    oleadas = [7,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,6,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,]
    #oleadas = [7,6,5,4,3,2,1,0]
    spawn = 30
    generation = 15
    fondotutorial=pygame.image.load("Miscelanea/fondotutorial.jpeg")
    '''--------------------------globales---------------------------------'''

    fuente= pygame.font.Font(None, 30)
    fuente2 = pygame.font.Font(None, 20)
    fondo=pygame.image.load("Miscelanea/mapa.png")
    fondomapa=pygame.image.load("Miscelanea/fondomapa.png")
    gameover=pygame.image.load("Miscelanea/gameover.png")
    principal=pygame.image.load("Miscelanea/principal.png")
    continuar=pygame.image.load("Miscelanea/continuar.png")
    reiniciar=pygame.image.load("Miscelanea/reiniciar.png")
    tutorial=pygame.image.load("Miscelanea/tutorial.png")
    salir=pygame.image.load("Miscelanea/salir.png")
    cursor=pygame.image.load("Miscelanea/cursor.png")
    cursor2=pygame.image.load("Miscelanea/cursor2.png")
    moneypng=pygame.image.load("Sprites/Money.png")
    ost=pygame.mixer.Sound("Sonidos/ost.ogg")
    ostgo=pygame.mixer.Sound("Sonidos/GameOver.ogg")

    ost.play(-1) #asi se reproduce indefinidamente
    infon=fondo.get_rect()
    #ost.set_volume(0.2)
    spritesaliados = []
    '''recortes de todos los sprites aliados en la funcion recorte'''
    spritesaliados.append(recorte.recorte(pygame.image.load("Sprites/marco.png"),[3,8,7,2],8,4))
    spritesaliados.append(recorte.recorte(pygame.image.load("Sprites/ZombieTarma.png"),[12,24,12,11],24,4))
    spritesaliados.append(recorte.recorte(pygame.image.load("Sprites/haduken.png"),[4,13,5,7],13,4))
    spritesaliados.append(recorte.recorte(pygame.image.load("Sprites/tanque1.png"),[4,14,6,4],14,4))
    spritesaliados.append(recorte.recorte(pygame.image.load("Sprites/MetalSlug.png"),[8,21,16],21))

    spritesenemigos = []
    '''-----------recortes de todos los sprites enemigos en la funcion recorte'''
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/arabe.png"),[4,12,8,4],12,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/soldier.png"),[4,12,11],12,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/gunner.png"),[8,16,17,4],17,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/ufo.png"),[8,8,8,7],8,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/alien.png"),[16,16,17,21],21,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/towertank.png"),[2,6,6,6],6,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/cangrejo.png"),[7,12,12,7],12,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load("Sprites/metalreal.png"),[5,7,31],31,4))


    sonialiadosatk = []
    '''--------------------Sonidos atauqe------------------------'''
    sonialiadosatk.append(pygame.mixer.Sound("Sonidos/marcoatk.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound("Sonidos/zombiedisparo.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound("Sonidos/ataqueprisionero.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound("Sonidos/tanque1ataque.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound("Sonidos/sfx_tanque.ogg"))


    sonialiadosmuerte = []
    '''--------------------Sonidos Muerte------------------------'''
    sonialiadosmuerte.append(pygame.mixer.Sound("Sonidos/muertemarco.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound("Sonidos/muertzombie.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound("Sonidos/muertearabe.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound("Sonidos/tanque1muerte.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound("Sonidos/tanquemuerte.ogg"))

    sonienemigoatk = []
    '''--------------------Sonidos atauqe------------------------'''
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/arabeatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/soldadoatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/ataquegunner.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/ataqueufo.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/ataquealien.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/towertankatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/cangrejoatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound("Sonidos/metalrealatk.ogg"))
    


    sonienemigomuerte = []
    '''--------------------Sonidos Muerte------------------------'''
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/muertearabe.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/soldadomuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/metralladoramuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/muertealienyufo.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/muertealienyufo.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/towertankmuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/cangrejomuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound("Sonidos/metalrealmuerte.ogg"))



    txt_salud=fuente.render("Salud", False, ROJO)
    txt_dama=fuente.render("Golpe", False, VERDE)
    txt_costo=fuente.render("Costo", False, DORADO)


    #grupo general
    todos = pygame.sprite.Group()
    aliados = pygame.sprite.Group()
    Selaliados = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    fuerte1 = fuerte()
    todos.add(fuerte1)
    fuerte2 = fuerte()
    fuerte2.image = pygame.image.load("Sprites/Fuerte2.png")
    fuerte2.rect.x = 1884
    todos.add(fuerte2)

    #aliados
    for i in range (5):
        b = SelectAliado(i+1)
        b.rect.x = 81*i+150
        b.rect.y = Alto - 70
        b.image = spritesaliados[i][0][0]
        Selaliados.add(b)

    pos_y,pos_x=250,200
    reloj=pygame.time.Clock()
    pygame.display.flip()
    fin = False
    pedro = 0
    pausa = True
    punt1 = MaCursor(cursor)
    punt1.rect.x=8
    punt2 = MaCursor(cursor2)
    punt2.rect.x=162
    menu.add(punt1)
    menu.add(punt2)
    aux = 0
    findg = False #Fin de juego
    findgd = False #Fin de juego derrota
    findgv = True #Fin de juego victoria
    reprod = False
    money = 0
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if punt1.rect.y == 90:
                        pausa = not pausa
                    elif punt1.rect.y == 210:
                        fin = True
                    elif punt1.rect.y == 170:
                        entuto = not entuto
                    if punt1.rect.y == 130:
                        for a in aliados:
                            aliados.remove(a)
                            todos.remove(a)
                        for e in enemigos:
                            enemigos.remove(e)
                            todos.remove(e)
                        fuerte1.vida = 500
                        fuerte2.vida = 2000
                        entuto = False
                        oleadas = [7,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,6,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,]
                        #oleadas = [7,6,5,4,3,2,1,0]
                        spawn = 30
                        generation = 15
                        money = 0

                if event.key == pygame.K_UP:
                    for e in menu:
                        e.opu = True
                if event.key == pygame.K_DOWN:
                    for e in menu:
                        e.opa = True
            if event.type == pygame.KEYUP:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for b in Selaliados:
                    if b.rect.collidepoint(pos):
                        if b.click and money >= stats[2][b.id-1]:
                            b.click = False
                            ali = Aliado(spritesaliados[b.id-1])
                            ali.damage = ali.damage[b.id-1]
                            ali.espera = ali.espera[b.id-1]
                            ali.vida = ali.vida[b.id-1]
                            ali.radius = ali.radius[b.id-1]
                            ali.precio = ali.precio[b.id-1]
                            ali.sonatk = sonialiadosatk[b.id-1]
                            ali.sonmuerte = sonialiadosmuerte[b.id-1]
                            money -= stats[2][b.id-1]
                            if b.id == 4:
                                ali.rect.y = Alto - 210
                            elif b.id == 5:
                                ali.rect.y = ali.rect.y - 10
                            aliados.add(ali)
                            todos.add(ali)
                            ali.rect.x=fonx+50

            if event.type == pygame.MOUSEBUTTONUP:
                for c in enemigos:
                    c.click = False
                for b in Selaliados:
                    b.click = True


        if pausa == False:
            ###########Limitadores de pantalla en X ############
            posm=list(pygame.mouse.get_pos())
            if posm[0]>Ancho-50:
                if(fonx-5>=Ancho-infon[2]):
                    fonx-=10
                    lsmov=todos
                    for e in lsmov:
                        e.rect.x-=10

            if posm[0]<50:
                if(fonx+15<=0):
                    fonx+=10
                    lsmov=todos
                    for e in lsmov:
                        e.rect.x+=10

            ###########Limitadores de pantalla en X ############
            if money < 1000:
                money += 1

            pantalla.fill(NEGRO)
            pantalla.blit(fondomapa,[0,0])
            pantalla.blit(fondo,[fonx,fony])

            #Generacion de enemigos
            if generation == 0:
                if len(oleadas) > 0:
                    enemy = oleadas.pop()
                    generation = (enemy+1)*spawn
                    c = Enemigo(spritesenemigos[enemy])
                    c.id = enemy
                    c.radius = c.radius[enemy]
                    c.damage = c.damage[enemy]
                    c.espera = c.espera[enemy]
                    c.vida = c.vida[enemy]
                    c.sonatk = sonienemigoatk[enemy]
                    c.sonmuerte = sonienemigomuerte[enemy]
                    enemigos.add(c)
                    todos.add(c)
                    c.rect.x,c.rect.bottom=infon[2]+fonx-100,Alto-134
                elif len(oleadas) == 0:
                    findgv = True
                    findg = True
                    pausa = True

            else:
                generation -=1

            #Colision enemigo llega a rango aliado
            for e in enemigos:
                for a in aliados:
                    if a.vida > 0 and e.vida > 0:
                        alcance=pygame.sprite.collide_circle(e,a)
                        if alcance:
                            for i9 in range (e.vida):
                                pygame.draw.circle(pantalla, ROJO, [5+e.rect.left+i9*7, e.rect.top-5], 2)
                            a.vel_x = 0
                            a.accion = 0
                            if a.attack:
                                a.accion = 2
                            if a.espera[0]<=0:
                                a.i = 0
                                e.vida-=a.damage
                                a.sonatk.play()
                                a.attack = True
                                a.espera[0]=a.espera[1]
                            else:
                                a.espera[0]-=1

                #Colision aliado llega a rango enemigo
            for a in aliados:
                for e in enemigos:
                    if a.vida > 0 and e.vida > 0:
                        alcance=pygame.sprite.collide_circle(a,e)
                        if alcance:
                            for i9 in range (a.vida):
                                pygame.draw.circle(pantalla, VERDE, [5+a.rect.left+i9*7, a.rect.top-5], 2)
                            e.vel_x = 0
                            e.accion = 0
                            if e.attack:
                                e.accion = 2
                            if e.espera[0]<=0:
                                e.i = 0
                                e.sonatk.play()
                                a.vida-=e.damage
                                e.attack = True
                                e.espera[0]=e.espera[1]
                            else:
                                e.espera[0]-=1

            #Colision enemigo llega a fuerte aliado
            for e in enemigos:
                a=fuerte1
                if a.vida > 0 and e.vida > 0:
                    alcance=pygame.sprite.collide_circle(a,e)
                    if alcance:
                        for i in range (a.vida):
                            pygame.draw.circle(pantalla, ROJO, [a.rect.left+i, a.rect.top-5], 2)
                        e.vel_x = 0
                        e.accion = 0
                        if e.attack:
                            e.accion = 2
                        if e.espera[0]<=0:
                            e.i = 0
                            e.sonatk.play()
                            a.vida-=e.damage
                            e.attack = True
                            e.espera[0]=e.espera[1]
                        else:
                            e.espera[0]-=1
                elif a.vida<=0:
                    findg = True
                    findgd = True
                    pausa = True

            for e in aliados:
                a=fuerte2
                if a.vida > 0 and e.vida > 0:
                    alcance=pygame.sprite.collide_circle(a,e)
                    if alcance:
                        for i in range (a.vida):
                            pygame.draw.circle(pantalla, ROJO, [a.rect.left+i, a.rect.top-5], 2)
                        e.vel_x = 0
                        e.accion = 0
                        if e.attack:
                            e.accion = 2
                        if e.espera[0]<=0:
                            e.i = 0
                            e.sonatk.play()
                            a.vida-=e.damage
                            e.attack = True
                            e.espera[0]=e.espera[1]
                        else:
                            e.espera[0]-=1
                elif a.vida<=0:
                    findg = True
                    findgv = True
                    pausa = True
            #Eliminacion vida=0
            for a in aliados:
                for e in enemigos:
                    if e.vida <= 0 or a.vida <= 0:
                        for a2 in aliados:
                            a2.vel_x = 4
                            a2.accion = 1
                        for e2 in enemigos:
                            e2.vel_x = -4
                            e2.accion = 1
                        if e.vida<=0:
                            e.sonmuerte.play()
                            enemigos.remove(e)
                            todos.remove(e)
                        if a.vida<=0:
                            a.sonmuerte.play()
                            aliados.remove(a)
                            todos.remove(a)

            pygame.draw.polygon(pantalla, NEGRO, [(0,Alto-120),(0,Alto),(Ancho,Alto),(Ancho,Alto-120)])
            pantalla.blit(txt_salud,[30, Alto-90])
            pantalla.blit(txt_dama,[30, Alto-70])
            pantalla.blit(txt_costo,[30, Alto-50])
            pantalla.blit(moneypng,[600, Alto-90])
            moneytxt = fuente.render(str(money), False, DORADO)
            pantalla.blit(moneytxt,[665, Alto-50])

            for b in Selaliados:
                txt_vsalud = fuente2.render(str(stats[0][b.id-1]), False, ROJO)
                pantalla.blit(txt_vsalud,[b.rect.x+15, b.rect.y-34])
                txt_vdama = fuente2.render(str(stats[1][b.id-1]), False, VERDE)
                pantalla.blit(txt_vdama,[b.rect.x+15, b.rect.y-22])
                txt_vcosto = fuente2.render(str(stats[2][b.id-1]), False, DORADO) #Cambiar b.damage por b.costo
                pantalla.blit(txt_vcosto,[b.rect.x+15, b.rect.y-10]) #mostrar atributos de los seleccionables
            todos.update()
            todos.draw(pantalla)
            enemigos.draw(pantalla)
            aliados.draw(pantalla)
            Selaliados.draw(pantalla)
            pygame.display.flip()
            reloj.tick(15)

        elif pausa == True and entuto == True: #Nueva linea 386
            pantalla.fill(NEGRO) #Nueva linea 387
            pantalla.blit(fondotutorial,[0,0]) #Nueva linea 388
            punt1.rect.y = 170 #Nueva linea 389
            pygame.display.flip() #Nueva linea 390

        elif pausa == True and findg == False:
            pantalla.fill(NEGRO)
            pantalla.blit(principal,[90,27])
            pantalla.blit(continuar,[30,90])
            pantalla.blit(reiniciar,[30,130])
            pantalla.blit(tutorial,[30,170])
            pantalla.blit(salir,[30,210])
            menu.update()
            menu.draw(pantalla)
            pygame.display.flip()

        elif pausa == True and findg == True:
            if findgd == True:
                pantalla.fill(NEGRO)
                ost.stop()
                pantalla.blit(gameover,[0,0])
                pygame.display.flip()
                if reprod == False:
                    ostgo.play()
                    reprod = True
            elif findgv == True:
                pantalla.fill(NEGRO)
                ostvictoria=pygame.mixer.Sound("Sonidos/Victoria.ogg")
                victoriaimagen=pygame.image.load("Miscelanea/fotovictoria.jpeg")
                pantalla.blit(victoriaimagen,[0,0])
                pygame.display.flip()
                if reprod == False:
                    ostvictoria.play()
                    reprod = True
