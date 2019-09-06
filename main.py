import pygame
import os
import random


pygame.init()                           # inicjalizacja modułu

szer = 600                              # wymiary okna
wys = 600

okno = pygame.display.set_mode((szer, wys))         # okno


def napisz(tekst, rozmiar, czy_srodek=True, x=0, y=0):       # funkcja pisząca w oknie
    cz = pygame.font.SysFont("Arial", rozmiar)      # tworzenie obiektu renderujacego napis odpowiednią czcionką
    rend = cz.render(tekst, 1, (255, 100, 100))
    if czy_srodek == True:
        x = (szer - rend.get_rect().width)/2
        y = (wys - rend.get_rect().height)/2        # wyśrodkowujemy napis
        okno.blit(rend, (x, y))                     # umieszczanie napisu w oknie graficznym
    elif czy_srodek == False:
        okno.blit(rend, (x, y))


copokazuje = "menu"
przeszkody = []


class przeszkoda:
    def __init__(self, x, szerokosc, odstep, kolor):
        self.x = x
        self.szerokosc = szerokosc
        self.y_gora = 0
        self.wys_gora = random.randint(150, 250)
        self.odstep = odstep
        self.y_dol = self.wys_gora + self.odstep
        self.wys_dol = wys - self.y_dol
        self.kolor = kolor
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)

    def rysuj(self):
        pygame.draw.rect(okno, self.kolor, self.ksztalt_gora, 0)
        pygame.draw.rect(okno, self.kolor, self.ksztalt_dol, 0)

    def ruch(self, v):
        self.x = self.x - v
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)

    def kolizja(self, player):
        if self.ksztalt_gora.colliderect(player) or self.ksztalt_dol.colliderect(player):
            return True
        else:
            return False

    def usun_przeszkody(self):
        for prz in przeszkody:
            przeszkody.remove(prz)


class helikoptr:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wys = 40
        self.szer = 45
        self.ksztalt = pygame.Rect(self.x, self.y, self.szer, self.wys)
        self.grafika = pygame.image.load(os.path.join('helikoptr.png'))

    def rysuj(self):
        okno.blit(self.grafika, (self.x, self.y))

    def ruch(self, v):
        self.y = self.y + v
        self.ksztalt = pygame.Rect(self.x, self.y, self.szer, self.wys)


class level:
    def __init__(self, poziom):
        self.poziom = poziom
        self.odstepy = [240, 230, 220, 210, 200, 190, 180, 170, 160]
        self.odstep = self.odstepy[self.poziom]
        self.kolor = (255, 255, 255)

    def zrob_przeszkody(self, czy_jedna, ilosc=0):
        if czy_jedna == False:
            for i in range(ilosc):
                przeszkody.append(przeszkoda(i*szer/20, szer/20, self.odstep, self.kolor))
        elif czy_jedna == True:
            przeszkody.append(przeszkoda(szer, szer/20, self.odstep, self.kolor))

    def zmien_level(self):
        self.kolor = (255-(self.poziom*2), 255-(self.poziom*10), 255)
        if self.poziom < 9:
            self.odstep = self.odstepy[self.poziom]


poz = level(0)
poz.zrob_przeszkody(False, 21)

gracz = helikoptr(250, 275)
dy = 0
punkty = 0
temp = 0

while True:                                         # pętla główna
    for event in pygame.event.get():

        if event.type == pygame.QUIT:               # wylaczenie przyciskiem X
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -1
            if event.key == pygame.K_DOWN:
                dy = 1
            if event.key == pygame.K_m:
                copokazuje = "menu"
    okno.fill((0, 0, 0))
    if copokazuje == "menu":                                                # MENU
        napisz("Naciśnij SPACJĘ, aby rozpocząć", 20, False, 200, 400)
        grafika = pygame.image.load(os.path.join('logo.png'))
        okno.blit(grafika, (0, 0))
        poz.poziom = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                copokazuje = "rozgrywka"

    elif copokazuje == "rozgrywka":                                         # GRA
        if poz.poziom > 8:
            copokazuje = "zwyciestwo"
        gracz.rysuj()
        gracz.ruch(dy)

        for p in przeszkody:                                                # rysowanie przeszkod
            p.rysuj()
            p.ruch(1)
            if p.kolizja(gracz.ksztalt):
                copokazuje = "koniec"

        for p in przeszkody:                                                # nowe przeszkody i usuwanie starych
            if p.x <= -p.szerokosc:
                przeszkody.remove(p)
                poz.zrob_przeszkody(True)
                punkty += abs(dy)
                temp += abs(dy)
        napisz(str(punkty), 25, 0, 20, 20)
        napisz("LEVEL " + str(poz.poziom), 30, False, 500, 550)

        if temp >= 35:                                                      # ilosc punktow na level
            poz.poziom += 1
            temp = 0
            poz.zmien_level()

    elif copokazuje == "koniec":                                            # KONIEC
        napisz("GAME OVER", 40)
        napisz("Aby udać się do menu, naciśnij M",15, 0, 215, 400)

        gracz = helikoptr(250, 275)
        dy = 0
        punkty = 0
        poz.poziom = 0
        poz.kolor = (255, 255, 255)
        for p in przeszkody:
            przeszkody.remove(p)
        poz.odstep = poz.odstepy[poz.poziom]
        poz.zrob_przeszkody(False, 21)

    elif copokazuje == "zwyciestwo":
        napisz("Aby udać się do menu, naciśnij M", 15, 0, 215, 400)
        grafika = pygame.image.load(os.path.join('wygrana.png'))
        okno.blit(grafika, (0, 30))

        gracz = helikoptr(250, 275)
        dy = 0
        punkty = 0
        poz.poziom = 0
        poz.kolor = (255, 255, 255)
        for p in przeszkody:
            przeszkody.remove(p)
        poz.odstep = poz.odstepy[poz.poziom]
        poz.zrob_przeszkody(False, 21)

    pygame.display.update()                         # odświeżanie ekranu
