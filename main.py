import pygame
from pygame.locals import *
import sys
import random



pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

# DEFINING THE PLAYABLE AREA
HEIGHT = 450
WIDTH = 1080
ACC = 0.5
FRIC = -0.12
FPS = 240

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# GENERATING THE PLAYER
playerSprite = pygame.image.load("playerSprite.png")
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load("character.png")
        self.image = playerSprite
        self.rect = self.image.get_rect()

        self.pos = vec((10, 360))
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

# CHECKS FOR COLLISION UPDATES
    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1

# GENERATES THE PLATFORM
platformSprite = pygame.image.load("platformSprite.png")
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = platformSprite
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT - 10))

    def move(self):
        pass


PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

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

    for entity in all_sprites:
        displaysurface.blit(entity.image, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)