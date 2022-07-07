import pygame
from pygame.locals import *
import math
import sys
import random
import time

### IMPORTANT ||| USE "python3 main.py" TO RUN THE PROGRAM

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

# DEFINING THE PLAYABLE AREA
HEIGHT = 1720
WIDTH = 1720
ACC = 0.5
FRIC = -0.12
FPS = 240
Score = 0
FramePerSec = pygame.time.Clock()

clock = pygame.time.Clock()
displaysurface = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Game")
#pygame.mixer.music.load("music.mp3")
#pygame.mixer.music.play()

def scrollY(screenSurf, offsetY):
    WIDTH, HEIGHT = screenSurf.get_size()
    copySurf = screenSurf.copy()
    screenSurf.blit(copySurf, (10, offsetY))

# GENERATING THE PLAYER
playerSprite = pygame.image.load("playerSprite.png")
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = playerSprite
        self.rect = self.image.get_rect()
        self.pos = vec((360, 560))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

# MOVE CONTROLS
    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

# JUMP CONTROLS
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15
            #scrollY(displaysurface, -50)
            #pygame.display.update()
            #for entity in all_sprites:
                #displaysurface.blit(entity.image, entity.rect)
                #entity.pos += vec(0, -100)


# CHECKS FOR COLLISION UPDATES
    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1

# GENERATES THE PLATFORM
platformSprite = pygame.image.load("platformSprite2.png")
class platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = vec(x, y)
        self.image = platformSprite
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        pass

# GENERATES THE COINS
coin = pygame.image.load("coin.png")
class object(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = vec(x, y)
        self.image = coin
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        pass


randomX = random.randint(200, 420)
randomY = random.randint(220, 300)
randomX2 = random.randint(100, 720)
randomY2 = random.randint(0, 0)
#  (left | right , up | down)
PT1 = platform(360, 560)
PT2 = platform(randomX, randomY)
PT3 = platform(randomX2, randomY2)
P1 = Player(360, 460)
C1 = object(randomX, randomY - 100)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(PT2)
all_sprites.add(P1)
all_sprites.add(C1)
all_sprites.add(PT3)

platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)
platforms.add(PT3)

myfont = pygame.font.SysFont(None, 30)
myfont2 = pygame.font.SysFont(None, 100)
while True:
    pressed_keys = pygame.key.get_pressed()
    displaysurface.fill((0, 0, 0))
    P1.update()
    if abs(P1.pos[0] - C1.pos[0]) < 75 and abs(P1.pos[1] - C1.pos[1]) < 75:
        Score += 1
        print(Score)
    print(P1.pos[0], P1.pos[1])
    if P1.pos[1] > 720:
        deathtext = myfont2.render('YOU DIED', True, (255, 100, 100))
        displaysurface.blit(deathtext, (200, 300))

    if pressed_keys[K_e]:
        FPS = 10
        #scrollY(displaysurface, -50)
        #pygame.display.update()
        freeze = myfont.render('SlowMo', True, (255, 100, 100))
        displaysurface.blit(freeze, (610, 60))
    else:
        FPS = 240


    for entity in all_sprites:
        displaysurface.blit(entity.image, entity.rect)
        entity.move()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
# 1 charactar = 10
    mytext = myfont.render('score: ' + str(Score), True, (255, 100, 100))
    mytext2 = myfont.render('X: ' + str(P1.pos[0] // 1), True, (255, 100, 100))
    mytext3 = myfont.render('Y: ' + str(P1.pos[1] // 1), True, (255, 100, 100))
    displaysurface.blit(mytext, (610, 1))
    if pressed_keys[K_q]:
        displaysurface.blit(mytext2, (610, 20))
        displaysurface.blit(mytext3, (610, 40))
    pygame.display.update()
    FramePerSec.tick(FPS)
