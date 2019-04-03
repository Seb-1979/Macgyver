# coding: utf-8
import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Vect
import os
import sys

SIDE_SPRITE = 50
NUM_SPRITE = 15
BOARD_SIZE = (SIDE_SPRITE*NUM_SPRITE, SIDE_SPRITE*NUM_SPRITE)
BACKGROUND_COLOR = (255, 255, 255)
PIECE_COLOR = (0, 0, 0)
CAPTION = "Déplacement d'une image"
MAP = []
WALL = 0
GROUND = 1
MACGYVER = 2
GUARDIAN = 3

def load_map(fname):
    with open(fname, "r") as file:
        for line in file:
            list = line.rstrip().split()
            MAP.append([int(c) for c in list])

class GamePlayer(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.step = 5
        self.image = image
        self.board_rect = pg.Rect((0, 0), BOARD_SIZE)
        self.rect = image.get_rect()

    def move(self, dx, dy):
        new_pos = pg.Rect(self.rect)
        new_pos.x += dx * SIDE_SPRITE
        new_pos.y += dy * SIDE_SPRITE
        if self.board_rect.contains(new_pos):
            self.rect.move_ip(dx * SIDE_SPRITE, dy * SIDE_SPRITE)


class GameGuardian(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()


class GameWall(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.move_ip(x * SIDE_SPRITE, y * SIDE_SPRITE)
    
        
class GameBoard(pg.sprite.Sprite):
    def __init__(self, images, player, guard, gp_walls):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(screen.get_size())
        self.rect = self.image.get_rect()

        load_map("map1.csv")
        for r in range(NUM_SPRITE):
            for c in range(NUM_SPRITE):
                if MAP[r][c] == MACGYVER:
                    player.move(c, r)
                    self.image.blit(images[GROUND], (c * SIDE_SPRITE, r * SIDE_SPRITE))
                elif MAP[r][c] == GUARDIAN:
                    guard.rect.move_ip(c * SIDE_SPRITE, r * SIDE_SPRITE)
                    self.image.blit(images[GROUND], (c * SIDE_SPRITE, r * SIDE_SPRITE))
                    self.image.blit(images[GUARDIAN], (c * SIDE_SPRITE, r * SIDE_SPRITE))
                elif MAP[r][c] == GROUND:
                    self.image.blit(images[GROUND], (c * SIDE_SPRITE, r * SIDE_SPRITE))
                else: # MAP[r][c] = WALL
                    gp_walls.add(GameWall(images[WALL], c, r))
                    self.image.blit(images[WALL], (c * SIDE_SPRITE, r * SIDE_SPRITE))


pg.init()
screen = pg.display.set_mode(BOARD_SIZE)
pg.display.set_caption(CAPTION)
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.USEREVENT])

images = []
images.append(pg.image.load("wall.jpg").convert())
images.append(pg.image.load("ground.jpg").convert())
images.append(pg.image.load("MacGyver.png").convert_alpha())
images.append(pg.image.load("Guardian.png").convert_alpha())

player = GamePlayer(images[MACGYVER])
guard = GameGuardian(images[GUARDIAN])
gp_walls = pg.sprite.Group()
board = GameBoard(images, player, guard, gp_walls)
gp_sprites_todraw = pg.sprite.Group([board, player])

clock = pg.time.Clock()
while 1:
#    clock.tick(60)
    for evt in pg.event.get():
        if evt.type == QUIT:
            pg.quit()
        elif evt.type == KEYDOWN:
            if evt.key == K_UP:
                player.move(0, -1)
                if pg.sprite.spritecollideany(player, gp_walls):
                    player.move(0, 1)
            elif evt.key == K_DOWN:
                player.move(0, 1)
                if pg.sprite.spritecollideany(player, gp_walls):
                    player.move(0, -1)
            elif evt.key == K_LEFT:
                player.move(-1, 0)
                if pg.sprite.spritecollideany(player, gp_walls):
                    player.move(1, 0)
            elif evt.key == K_RIGHT:
                player.move(1, 0)
                if pg.sprite.spritecollideany(player, gp_walls):
                    player.move(-1, 0)

    gp_sprites_todraw.draw(screen)
    pg.display.update()