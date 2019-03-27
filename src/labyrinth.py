# coding : utf-8

import os
import random
from pygame.math import Vector2 as vect
from copy import copy

WALL = 0
GROUND = 1
MACGYVER = 2
GUARDIAN = 3
SIDE = 15

class Labyrinth:
	def __init__(self):
		self.map = []
		
	def load_map(self, fname):
		self.map = []
		with open(fname, "r") as file:
			for line in file:
				list = line.rstrip().split()
				self.map.append([int(c) for c in list])
	
		return self.map
	
	''' Création d'un labyrinthe dont le point de départ est le coin
		supérieur gauche et la sortie à l'angle opposé
	'''
	def autocreate_map_save(self):
		self.map = [[WALL for _ in range(SIDE)] for _ in range(SIDE)]
		pos = vect(0,0)
		end = vect(14,14)
		delta_h = vect(0,1) #déplacement d'une case horizontalement
		delta_v = vect(1,0) #déplacement d'une case verticalement

		self.map[int(pos[0])][int(pos[1])] = GROUND
		flag = 0
		#on augmente la probabilité d'aller à droite ou en bas par rapport
		while pos != end:
			flag += 1
			
			direction = [] #contient les nouvelles positions possibles
			#peut-on aller à gauche
			p = pos - delta_h
			p = eval(p.__str__())
			if p[1] != -1 and self.map[p[0]][p[1]] != GROUND:
				direction.append(p)
			#peut-on aller en haut
			p = pos - delta_v
			p = eval(p.__str__())
			if p[0] != -1 and self.map[p[0]][p[1]] != GROUND:
				direction.append(p)
			#peut-on aller à droite
			p = pos + delta_h
			p = eval(p.__str__())
			if p[1] != 15 and self.map[p[0]][p[1]] != GROUND:
				direction.extend([p, p])
			#peut-on aller en bas
			p = pos + delta_v
			p = eval(p.__str__())
			if p[0] != 15 and self.map[p[0]][p[1]] != GROUND:
				direction.extend([p, p])
			
			n = len(direction)
			if n > 0:
				if n == 1:
					pos = direction[0]
				else:
					random.seed()
					random.shuffle(direction)
					pos  = random.choice(direction)
				self.map[pos[0]][pos[1]] = GROUND
			else:
				print("l'algorithme n'a pas convergé")
				print("Nombre de tours : ", flag)
				return False
		
		print("Nombre de tours : ", flag)
		
		return True

	def autocreate_map(self):
		self.map = [[-1 for _ in range(SIDE)] for _ in range(SIDE)]
		self.map[14][12] = WALL
		self.map[13][14] = WALL
		pos = vect(0,0)
		end = vect(14,14)
		delta_h = vect(0,1) #déplacement d'une case horizontalement
		delta_v = vect(1,0) #déplacement d'une case verticalement

		self.map[int(pos[0])][int(pos[1])] = GROUND
		flag = 0
		#on augmente la probabilité d'aller à droite ou en bas par rapport
		random.seed()
		while pos != end:
			flag += 1
			
			direction = [] #contient les nouvelles positions possibles
			#peut-on aller à gauche
			p = pos - delta_h
			p = eval(p.__str__())
			if p[1] != -1 and self.map[p[0]][p[1]] != WALL:
				direction.append(p)
			#peut-on aller en haut
			p = pos - delta_v
			p = eval(p.__str__())
			if p[0] != -1:
				direction.append(p)
			#peut-on aller à droite
			p = pos + delta_h
			p = eval(p.__str__())
			if p[1] != 15 and self.map[p[0]][p[1]] != WALL:
				if p[1] > 7 and p[0] < 8:
					direction.append(p)
				else:
					direction.extend([p, p])
			#peut-on aller en bas
			p = pos + delta_v
			p = eval(p.__str__())
			if p[0] != 15 and self.map[p[0]][p[1]] != WALL:
				if p[0] > 7 and p[1] < 8:
					direction.append(p)
				else:
					direction.extend([p, p])
			
			#print(pos, " ", direction)
			n = len(direction)
			if n > 0:
				if n == 1:
					pos = direction[0]
				else:
					random.shuffle(direction)
					pos  = random.choice(direction)
				self.map[pos[0]][pos[1]] = GROUND
			else:
				print("l'algorithme n'a pas convergé")
				print("Nombre de tours : ", flag)
				return False
				
		print("Nombre de tours : ", flag)
		
		return True
			
def main():
	laby = Labyrinth()
	laby.autocreate_map()
	
	s = "   "
	for r in range(14):
		s = s + "{:2}".format(str(r)) + " "
	s = s + "14"
	print(s)
	l = 0
	
	for r in laby.map:
		s = ""
		s = s + "{:2}[".format(l)
		for c in r[:10]:
			s = s + "{:2}".format(str(c)) + " "
		for c in r[10:14]:
			s = s + "{:2}".format(c) + " "
		s = s + "{:2}]".format(r[-1])
		print(s)
		l += 1
		
if __name__ == "__main__":
    main()
