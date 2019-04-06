# coding: utf-8
import pygame as pg
from pygame.locals import *
import os

from constants import *
from game_items import *
from game_board import *
from labyrinth import *

def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(CAPTION)
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.USEREVENT])

    laby = Labyrinth()
    if not laby.load_map("maps/map_1.txt"):
        laby.autocreate_map()

    images = []
    images.append(pg.image.load("images/seringue.png").convert_alpha())
    images.append(pg.image.load("images/ether.png").convert_alpha())
    images.append(pg.image.load("images/tube.png").convert_alpha())
    items = Items(images, BOARD_SIDE, 0)
    gp_items = pg.sprite.Group(items)

    player = GamePlayer(pg.image.load("images/MacGyver.png").convert_alpha(), 0, 0)
    guard = SpriteBase(pg.image.load("images/Guardian.png").convert_alpha(), 14, 14)
    gp_walls = pg.sprite.Group()
    board = GameBoard(laby.map, gp_walls)

    gp_board_all = pg.sprite.Group([board, player, guard])

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

        gp_board_all.draw(screen)
        gp_items.update()
        gp_items.draw(screen)
        pg.display.update()

if __name__ == '__main__':
    main()