# coding: utf-8
import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Vect
import os
import sys

SIDE_SPRITE = 50
NUM_SPRITE = 15
BOARD_SIZE = (SIDE_SPRITE*NUM_SPRITE, SIDE_SPRITE*NUM_SPRITE)
CAPTION = "MACGYVER"
MAP = []
WALL = 0
GROUND = 1

def load_map(fname):
    with open(fname, "r") as file:
        for line in file:
            line = line.rstrip()
            MAP.append([int(c) for c in line])

class SpriteBase(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.move_ip(x * SIDE_SPRITE, y * SIDE_SPRITE)


class GamePlayer(SpriteBase):
    def __init__(self, image, x, y):
        SpriteBase.__init__(self, image, x, y)
        self.step = 5
        self.board_rect = pg.Rect((0, 0), BOARD_SIZE)

    def move(self, dx, dy):
        new_pos = pg.Rect(self.rect)
        new_pos.x += dx * SIDE_SPRITE
        new_pos.y += dy * SIDE_SPRITE
        if self.board_rect.contains(new_pos):
            self.rect.move_ip(dx * SIDE_SPRITE, dy * SIDE_SPRITE)


class GameBoard(pg.sprite.Sprite):
    def __init__(self, gp_walls):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(BOARD_SIZE)
        self.rect = self.image.get_rect()
        self.images = []
        self.images.append(pg.image.load("images/wall.jpg").convert())
        self.images.append(pg.image.load("images/ground.jpg").convert())


        load_map("maps/map_1.txt")
        for r in range(NUM_SPRITE):
            for c in range(NUM_SPRITE):
                if MAP[r][c] == GROUND:
                    self.image.blit(self.images[GROUND], (c * SIDE_SPRITE, r * SIDE_SPRITE))
                else: # MAP[r][c] = WALL
                    gp_walls.add(SpriteBase(self.images[WALL], c, r))
                    self.image.blit(self.images[WALL], (c * SIDE_SPRITE, r * SIDE_SPRITE))


def main():
    pg.init()
    screen = pg.display.set_mode(BOARD_SIZE)
    pg.display.set_caption(CAPTION)
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.USEREVENT])

    player = GamePlayer(pg.image.load("images/MacGyver.png").convert_alpha(), 0, 0)
    guard = SpriteBase(pg.image.load("images/Guardian.png").convert_alpha(), 14, 14)
    gp_walls = pg.sprite.Group()
    board = GameBoard(gp_walls)
    gp_sprites_todraw = pg.sprite.Group([board, player, guard])

    clock = pg.time.Clock()
    while 1:
        clock.tick(60)
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

if __name__ == '__main__':
    main()