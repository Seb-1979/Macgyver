# coding : utf-8

import os, random, math, re
from pygame.math import Vector2 as vect
import constants

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
	
	def save_map(self):
		dir_maps = "../maps/"
		if not os.access(dir_maps, os.F_OK):
			os.mkdir(dir_maps)
			fname = dirmaps + "map_1.txt"
		else:
			pattern = re.compile(r"^map_(?P<num>\d+)\.txt$")
			list_file = [pattern.match(f) for f in os.listdir(dir_maps)]
			num = sorted([int(f.group("num")) for f in list_file if f])
			print(num)
			if num:
				fname = dir_maps + "map_" + str(num[-1] + 1) + ".txt"
			else:
				fname = dir_maps + "map_1.txt"
		
		with open(fname, mode='w', encoding='utf-8') as file:
			for r in range(SIDE):
				for c in range(SIDE):
					file.write(str(self.map[r][c]))
				file.write("\n")
		print("Le labyrinthe a été sauvegardé dans le fichier ", fname, " avec succés.")
				
	''' Retoune un tuple contenant le signe de x et y
		le signe de a est donné par :
		-1 si a < 0
		 0 si a = 0
		 1 si a > 0
	'''
	def _symbol(self, v):
		if v[0] == 0:
			rx = 0
		else:
			rx = v[0] // (v[0] if v[0] > 0 else -v[0])
		if v[1] == 0:
			ry = 0
		else:
			ry = v[1] // (v[1] if v[1] > 0 else -v[1])
		return rx, ry
	
	def _frequency(self, v):
		gcd = math.gcd(int(v[0]),int(v[1]))
		s = self._symbol(v)
		if s == (1,1):   return (0, 0, int(v[1] / gcd), int(v[0] / gcd))
		if s == (1,0):   return (1,0,1,2)
		if s == (1,-1):  return (int(-v[1] / gcd), 0, 0, int(v[0] / gcd))
		if s == (0,1):   return (0,1,2,1)
		if s == (0,-1):  return (2,1,0,1)
		if s == (-1,1):  return (0, int(-v[0] / gcd), int(v[1] / gcd), 0)
		if s == (-1,0):  return (1,2,1,0)
		if s == (-1,-1): return (int(-v[1] / gcd), int(-v[0] / gcd), 0, 0)

	''' Création d'un chemin aléatoire entre les points p1 et p2
		p1 (list): coordonnées de départ dans self.map
		p2 (list): coordonnées d'arrivée dans self.map
	'''
	def _create_way(self, p1, p2):
		current_pos = vect(p1)
		end_pos = vect(p2)
		#ind = {"left": 0, "up": 1, "right": 2, "down": 3} #indices des directions
		''' Le tuple delta contient respectivement les vecteurs directeurs pour 
			aller à gauche, en haut, à droite et en bas. Ces vecteurs permettent
			de se déplacer dans self.map
		'''
		delta = (vect(0,-1), vect(-1,0), vect(0,1), vect(1,0))
		
		nb_tours = 0
		while current_pos != end_pos:
			Dv = end_pos - current_pos #direction vector
			
			freq = self._frequency(Dv)
			mv = [(eval((current_pos + delta[k]).__str__()), freq[k]) for k in range(4) if freq[k]]
			tmp = []
			for p, f in mv:
				if p[0] >= 0 and p[0] <= 14 and p[1] >= 0 and p[1] <= 14:
					tmp.extend([p for _ in range(f)])
			mv = tmp
			random.shuffle(mv)
			pos = random.choice(mv)
			self.map[pos[0]][pos[1]] = GROUND
			current_pos = vect(pos[0], pos[1])
			
			nb_tours += 1
			
		#print("Nombre de tours : ", nb_tours)
	
	''' Création d'un labyrinthe dont le point de départ est le coin
		supérieur gauche et la sortie à l'angle opposé
	'''
	def autocreate_map(self):
		self.map = [[WALL for _ in range(SIDE)] for _ in range(SIDE)]
		random.seed()

		list_pos = [
			[[0, 0], [14, 13]], #le gardien sera placé au point [14,14]
			[[0, 4], [14, 10]],
			[[0, 10], [14, 4]],
			[[14, 0], [0, 14]],
			[[4, 0], [10, 14]],
			[[10, 0], [4, 14]]
		]
		
		for start, end in list_pos:
			self.map[start[0]][start[1]] = GROUND
			self._create_way(start, end)

	def print_map(self):
		s = "   "
		for r in range(14):
			s = s + "{:2}".format(str(r)) + " "
		s = s + "14"
		print(s)
		l = 0
	
		for r in self.map:
			s = ""
			s = s + "{:2}[".format(l)
			for c in r[:10]:
				s = s + "{:2}".format(str(c)) + " "
			for c in r[10:14]:
				s = s + "{:2}".format(c) + " "
			s = s + "{:2}]".format(r[-1])
			print(s)
			l += 1
				
def main():
	laby = Labyrinth()
	laby.autocreate_map()
	laby.print_map()
	
	'''
	nb_wall = 0
	nb_ground = 0
	for r in laby.map:
		for c_r in r:
			if c_r == GROUND:
				nb_ground += 1
			else:
				nb_wall += 1
	print("Nombre de murs : {}, nombre de dalles : {}".format(nb_wall, nb_ground))
	'''
	
	answer = input("Faut-il enregistrer le labyrinthe dans un fichier [O]ui : ")
	pattern = re.compile(r"(o$)|oui", re.IGNORECASE)
	if pattern.match(answer):
		laby.save_map()
		
if __name__ == "__main__":
    main()
