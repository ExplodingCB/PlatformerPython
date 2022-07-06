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
black = (0,0,0)
FramePerSec = pygame.time.Clock()

clock = pygame.time.Clock()
displaysurface = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Game")

clock.tick(60)
pygame.display.update()

def scrollY(screenSurf, offsetY):
    width, height = screenSurf.get_size()
    copySurf = screenSurf.copy()
    screenSurf.blit(copySurf, (0, offsetY))
    if offsetY < 0:
        screenSurf.blit(copySurf, (0, height + offsetY), (0, 0, width, -offsetY))
    else:
        screenSurf.blit(copySurf, (0, 0), (0, height - offsetY, width, offsetY))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('font.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    displaysurface.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)


# GENERATING THE PLAYER
playerSprite = pygame.image.load("playerSprite.png")
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image = pygame.image.load("character.png")
        Player.x = x
        Player.y = y
        self.image = playerSprite
        self.rect = self.image.get_rect()
        self.pos = vec((360, 560))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

# MOVE CONTROLS
    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
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
            scrollY(displaysurface, -50)
            pygame.display.update()
            for entity in all_sprites:
                displaysurface.blit(entity.image, entity.rect)
                entity.pos.y += -50


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
        self.x = x
        self.y = y
        self.image = coin
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        pass




randomX = random.randint(200, 420)
randomY = random.randint(220, 300)
randomX2 = random.randint(100, 220)
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




while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()



    displaysurface.fill((0, 0, 0))
    P1.update()
    if abs(P1.pos[0] - C1.x) < 75 and abs(P1.pos[1] - C1.y) < 75:
        Score += 1
        print(Score)
    #print(P1.pos[0], P1.pos[1])
    if P1.pos[1] > 720:
        message_display("You Died")
        time.sleep(5)
        pygame.quit()



    for entity in all_sprites:
        displaysurface.blit(entity.image, entity.rect)
        entity.move()





    pygame.display.update()
    FramePerSec.tick(FPS)