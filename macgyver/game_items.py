# coding: utf-8
import pygame as pg
from pygame.locals import *
import os
from constants import *

class Items(pg.sprite.Sprite):
    def __init__(self, images, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(ITEMS_SIZE)
        self.image.fill((255, 255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.images = images
        self.items_found = []
        self.items_change = False

    def set_item(self, item):
        self.items_found.append(item)
        self.items_change = True

    def update(self):
        if self.items_change:
            self.image.blit(self.images[self.items_found[-1]],
                                        (0, (len(self.items_found) - 1) * SPRITE_SIDE))
            self.items_change = False


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Affichage des items")

    images = []
    images.append(pg.image.load("images/seringue.png").convert_alpha())
    images.append(pg.image.load("images/ether.png").convert_alpha())
    images.append(pg.image.load("images/tube.png").convert_alpha())
    items = Items(images, BOARD_SIDE, 0)
    gp_items = pg.sprite.Group(items)

    pg.display.update()

    it = 0

    clock = pg.time.Clock()
    loop = True
    while loop:
        clock.tick(60)
        for evt in pg.event.get():
            if evt.type == QUIT:
                loop = False
            elif evt.type == KEYDOWN:
                if evt.key == K_RETURN:
                    if it == 0:
                        items.set_item(SYRINGE)
                        it += 1
                    elif it == 1:
                        items.set_item(ETHER)
                        it += 1
                    elif it == 2:
                        items.set_item(TUBE)
                        it += 1
        gp_items.update()
        gp_items.draw(screen)
        pg.display.update()

if __name__ == '__main__':
    main()