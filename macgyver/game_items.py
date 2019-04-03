# coding: utf-8
import pygame as pg
from pygame.locals import *
import os
import constants
import labyrinth

SIDE_SPRITE = 50
NUM_SPRITE = SIDE
SCREEN_SIZE = (SIDE_SPRITE*NUM_SPRITE, SIDE_SPRITE*NUM_SPRITE)
BACKGROUND_COLOR = (255, 255, 255)
PIECE_COLOR = (0, 0, 0)
CAPTION = "Macgyver"

class GameUI:

	def __init__(self, screen):
		self.images = []
		self.images.append(pg.image.load("../textures/wall.jpg").convert())
		self.images.append(pg.image.load("../textures/ground.jpg").convert())
		self.laby = Labyrinth()
	
	def select_map(self)
		maps_dir = "../maps/"
		for file in os.listdir(maps_dir):
			try:
				laby.load_map(file)
		for r in range(NUM_SPRITE):
			for c in range(NUM_SPRITE):
				if MAP[r][c] == MapObj.ground:
					screen.blit(self.image, (c * SIDE_SPRITE, r * SIDE_SPRITE))


def main()		
	pg.init()
	screen = pg.display.set_mode(SCREEN_SIZE)
	pg.display.set_caption(CAPTION)
	background = Background(screen)
	pg.display.flip()

	clock = pg.time.Clock()
	loop = True
	while loop:
		clock.tick(60)
		for evt in pg.event.get():
			if evt.type == QUIT:
				loop = False
