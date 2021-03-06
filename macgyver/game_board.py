# coding: utf-8
import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Vect

import os
import sys

from constants import *


class SpriteBase(pg.sprite.Sprite):
    ''' Base class defining the sprites of the game.

        :param image: image of the sprite
        :type image: pygame.Surface
        :param x: index of the column in the maze's game
        :type x: int
        :param y: index of the row in the maze's game
        :type y: int
    '''
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.move_ip(x * SPRITE_SIDE, y * SPRITE_SIDE)


class GamePlayer(SpriteBase):
    ''' The class that defines the player of the game. It inherits from the
        SpriteBase class and uses the same initialization parameters.
    '''
    def __init__(self, image, x, y):
        SpriteBase.__init__(self, image, x, y)
        self.step = 5
        self.board_rect = pg.Rect((0, 0), (BOARD_SIDE, BOARD_SIDE))

    def move(self, dx, dy):
        ''' This function sets the player's movement of one square on the
            gameboard.

            :param dx: defined the horizontal displacement of one square
            :type dx: int
            :param dy: defined the vertical displacement of one square
            :type dy: int
        '''
        new_pos = pg.Rect(self.rect)
        new_pos.x += dx * SPRITE_SIDE
        new_pos.y += dy * SPRITE_SIDE
        if self.board_rect.contains(new_pos):
            self.rect.move_ip(dx * SPRITE_SIDE, dy * SPRITE_SIDE)


class GameBoard(pg.sprite.Sprite):
    ''' This class sets the display of the gameboard. It inherits from
        SpriteBase.

        :param map: two dimensional table indicating the position of all walls
                    by the value "GROUND" and the floor by the value "WALL" in
                    the labyrinth
        :type map: nested list in a list
        :param gp_walls: contains all the sprites of the walls
        :type gp_walls: pygame.sprite.Group
    '''
    def __init__(self, map, gp_walls):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((BOARD_SIDE, BOARD_SIDE))
        self.rect = self.image.get_rect()
        self.images = []
        self.images.append(pg.image.load("images/wall.jpg").convert())
        self.images.append(pg.image.load("images/ground.jpg").convert())

        for r in range(SPRITE_NUM):
            for c in range(SPRITE_NUM):
                if map[r][c] == GROUND:
                    self.image.blit(self.images[GROUND], (c * SPRITE_SIDE,
                                    r * SPRITE_SIDE))
                else:  # map[r][c] = WALL
                    gp_walls.add(SpriteBase(self.images[WALL], c, r))
                    self.image.blit(self.images[WALL], (c * SPRITE_SIDE,
                                    r * SPRITE_SIDE))


def main():
    pg.init()
    screen = pg.display.set_mode((BOARD_SIDE, BOARD_SIDE))
    pg.display.set_caption("Plateau du jeu")
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.USEREVENT])

    player = GamePlayer(pg.image.load("images/MacGyver.png").convert_alpha(),
                        0, 0)
    guard = SpriteBase(pg.image.load("images/Guardian.png").convert_alpha(),
                       14, 14)
    gp_walls = pg.sprite.Group()

    map = []
    with open("maps/map_1.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            map.append([int(c) for c in line])
    board = GameBoard(map, gp_walls)
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
