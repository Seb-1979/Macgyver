# coding: utf-8

import pygame as pg
from pygame.locals import *
from pygame.sprite import spritecollide, spritecollideany, collide_rect

import os
from sys import exit
from random import seed, randint

from constants import *
from game_items import *
from game_board import *
from labyrinth import *
from graphe import *

player_pos = (0, 0)
guard_pos = (14, 14)

pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption(CAPTION)
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.USEREVENT])

img = []
img.append(pg.image.load("images/seringue.png").convert_alpha())
img.append(pg.image.load("images/ether.png").convert_alpha())
img.append(pg.image.load("images/tube.png").convert_alpha())
img.append(pg.image.load("images/MacGyver.png").convert_alpha())
img.append(pg.image.load("images/Guardian.png").convert_alpha())


def get_coord_items():
    gph = Graph(laby.map, GROUND)
    sg = gph.sub_graph(player_pos)
    # we search all the paths of the graph starting from the coordinates of
    # the player
    ways = gph.search_ways(player_pos)
    seed()
    coord_items = []  # coordinates of each object of the game
    for k in [SYRINGE, ETHER, TUBE]:
        flag = True
        while flag:
            i = randint(0, len(ways) - 1)  # take a random path among ways
            w = ways[i]
            lg = len(w) - 1  # index of the last element of w
            # the object can not be placed at the player's position (way[0])
            # or guardian
            if w[lg] == guard_pos:
                j = randint(1, lg - 1)
            else:
                j = randint(1, lg)
            # we check that an object is not already placed at position w[j]
            if w[j] not in coord_items:
                flag = False
                coord_items.append(w[j])
    return tuple(coord_items)


laby = Labyrinth()
if not laby.load_map("maps/map_1.txt"):
    laby.autocreate_map()

# Creation of the border containing the objects collected by the player
items_collected = ItemsCollected(img, BOARD_SIDE, 0)
gp_items_collected = pg.sprite.Group([items_collected])

# Creation of all sprites of objects placed on the game board
pos_syr, pos_eth, pos_tub = get_coord_items()
sp_syr = SpriteBase(img[SYRINGE], pos_syr[1], pos_syr[0])
sp_eth = SpriteBase(img[ETHER], pos_eth[1], pos_eth[0])
sp_tub = SpriteBase(img[TUBE], pos_tub[1], pos_tub[0])
gp_items_onboard = pg.sprite.Group([sp_syr, sp_eth, sp_tub])

# Creation of the other sprites composing the game board
player = GamePlayer(img[MACGYVER], player_pos[1], player_pos[0])
guard = SpriteBase(img[GUARDIAN], guard_pos[1], guard_pos[0])
gp_walls = pg.sprite.Group()
board = GameBoard(laby.map, gp_walls)
gp_board_all = pg.sprite.Group([board, player, guard])

# Displayed image to indicate if the player has won or lost
final_img = pg.Surface(SCREEN_SIZE).convert_alpha()
final_img.fill((255, 255, 255, 127))

clock = pg.time.Clock()
loop = True  # its value goes to False when the player closes the game window
game = True  # its value goes to False when the player finishes the game
while loop:
    clock.tick(60)
    for evt in pg.event.get():
        if evt.type == QUIT:
            loop = False
        elif game and evt.type == KEYDOWN:
            player_mv = False  # its value is True if the player moves
            # We test if the player to press a direction key. Depending on the
            # direction taken, we move the player's sprite if it does not
            # collide with a wall
            if evt.key == K_UP:
                player.move(0, -1)
                if spritecollideany(player, gp_walls):
                    player.move(0, 1)
                else:
                    player_mv = True
            elif evt.key == K_DOWN:
                player.move(0, 1)
                if spritecollideany(player, gp_walls):
                    player.move(0, -1)
                else:
                    player_mv = True
            elif evt.key == K_LEFT:
                player.move(-1, 0)
                if spritecollideany(player, gp_walls):
                    player.move(1, 0)
                else:
                    player_mv = True
            elif evt.key == K_RIGHT:
                player.move(1, 0)
                if spritecollideany(player, gp_walls):
                    player.move(-1, 0)
                else:
                    player_mv = True
            if player_mv:  # le joueur se déplace
                # We test the collision between the player and an object of
                # the game board. In the case of a collision, sp contains the
                # sprite of the object and is removed from the group
                # gp_items_onboard
                sp = spritecollide(player, gp_items_onboard, True)
                if sp:
                    # According to the value of sp, we add the object
                    # recovered by the player in the border
                    if sp[0] == sp_eth:
                        items_collected.set_item(ETHER)
                    elif sp[0] == sp_tub:
                        items_collected.set_item(TUBE)
                    elif sp[0] == sp_syr:
                        items_collected.set_item(SYRINGE)
                # test of the collision between the player and the guardian
                if collide_rect(player, guard):
                    game = False
                    pg.font.init()
                    ft = pg.font.Font(pg.font.get_default_font(), 100)
                    if len(items_collected.items_found) == 3:
                        gp_board_all.remove([guard])
                        txt = ft.render("You win !!!", True,
                                        (0, 0, 0, 255))
                    else:
                        gp_board_all.remove([player])
                        txt = ft.render("You lose !!!", True,
                                        (0, 0, 0, 255))
                    txt_pos = ((SCREEN_SIZE[0] - txt.get_width()) // 2,
                               (SCREEN_SIZE[1] - txt.get_height()) // 2)
                    final_img.blit(txt, txt_pos)
                    pg.font.quit()

    # update the display
    gp_board_all.draw(screen)
    gp_items_onboard.draw(screen)
    gp_items_collected.update()
    gp_items_collected.draw(screen)
    if not game:
        screen.blit(final_img, (0, 0))
    pg.display.update()
