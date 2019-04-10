# coding : utf-8

import os
from random import shuffle, choice, seed
from math import gcd
from re import compile, IGNORECASE

from pygame.math import Vector2 as vect

from constants import *


class Labyrinth:
    ''' This class manages the creation, saving and loading of a maze for the
        game.

        :ivar map: Two dimensional table indicating the position of all walls
                   by the value "WALL" and the floor by the value "GROUND" in
                   the labyrinth.
        :vartype map: nested list in a list
    '''
    def __init__(self):
        self.map = []

    def load_map(self, fname):
        ''' This function initializes the map variable from the data saved in
            the "fname" file.

            :param fname: name of the file to load
            :type fname: string
            :return: returns True if the file loading went well
            :rtype: boolean
        '''
        self.map.clear()
        # a line in the file contains exactly 15 digits of value 0 or 1.
        # Spaces at the end of the line are ignored
        pattern = compile(r"^[01]{15}$")
        # indicates the number of lines read that must be 15
        num_row = 0
        with open(fname, "r") as file:
            try:
                for line in file:
                    line = line.rstrip()
                    if pattern.match(line):
                        self.map.append([int(c) for c in line])
                        num_row += 1
                    elif num_row > 15:
                        self.map.clear()
                        return False
                    else:
                        self.map.clear()
                        return False
            except Exception:
                self.map.clear()
                return False
        return True

    def save_map(self):
        ''' Save the map array to a file. The recording directory is maps. The
            files are named map_X.txt where X is a number.
        '''
        if not self.map:
            return False

        current_dir = os.path.dirname(__file__)
        maps_dir = os.path.join(current_dir, "maps")
        if not os.access(maps_dir, os.F_OK):
            os.mkdir(maps_dir)
            fname = os.path.join(maps_dir, "map_1.txt")
        else:
            pattern = compile(r"^map_(?P<num>\d+)\.txt$")
            list_file = [pattern.match(f) for f in os.listdir(maps_dir)]
            num = sorted([int(f.group("num")) for f in list_file if f])
            if num:
                fname = os.path.join(maps_dir, "map_" +
                                     str(num[-1]+1) +
                                     ".txt")
            else:
                fname = os.path.join(maps_dir, "map_1.txt")

        with open(fname, mode='w', encoding='utf-8') as file:
            for r in range(15):
                for c in range(15):
                    file.write(str(self.map[r][c]))
                file.write("\n")

        return True

    def _symbol(self, v):
        ''' Returns a tuple containing an indicator of the vector sign
            v = (rx, ry). The sign of a number N is given by:
                 -1 if N < 0
                 0 if N = 0
                 1 if N > 0
        '''
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
        ''' v is a director vector that is determined to have a probability
            of taking one of the four possible directions rather than another.
            The desired result is a tuple noted (Fl, Fu, Fr, Fd) where each
            element is the realization frequency to go to the left (Fl), to
            the top (Fu), to the right (Fr) and to the bottom (Fd) ). Noting
            F = Fl + Fu + Fr + Fd, the equivalence relation between frequency
            and probability is given by Pi = Fi / F where i = {l, u, r, d}.
        '''
        d = gcd(int(v[0]), int(v[1]))
        s = self._symbol(v)
        if s == (1, 1):
            return (0, 0, int(v[1]/d), int(v[0]/d))
        if s == (1, 0):
            return (1, 0, 1, 2)
        if s == (1, -1):
            return (int(-v[1]/d), 0, 0, int(v[0]/d))
        if s == (0, 1):
            return (0, 1, 2, 1)
        if s == (0, -1):
            return (2, 1, 0, 1)
        if s == (-1, 1):
            return (0, int(-v[0]/d), int(v[1]/d), 0)
        if s == (-1, 0):
            return (1, 2, 1, 0)
        if s == (-1, -1):
            return (int(-v[1]/d), int(-v[0]/d), 0, 0)

    def _create_way(self, p1, p2):
        ''' Creating a random path between points p1 and p2. The coordinates
            are given in a list.
        '''
        current_pos = vect(p1)  # current position
        end_pos = vect(p2)  # final position
        # The delta tuple contains normative vectors, respectively, to go to
        # the left, top, right, and bottom. These vectors allow to move in
        # self.map
        delta = (vect(0, -1), vect(-1, 0), vect(0, 1), vect(1, 0))

        while current_pos != end_pos:
            # vector director between point current_pos and end_pos
            Dv = end_pos - current_pos
            freq = self._frequency(Dv)
            # mv contains a tuple list for each possible direction. Each
            # tuple contains the new current position and its frequency of
            # realization.
            mv = [(eval((current_pos+delta[k]).__str__()), freq[k])
                  for k in range(4) if freq[k]]
            tmp = []  # list containing all possible achievements
            for p, f in mv:
                # we check that the new position is well included in map. If
                # this condition is respected, we add f (frequency) times the
                # position p in tmp
                if 0 <= p[0] <= 14 and 0 <= p[1] <= 14:
                    tmp.extend([p for _ in range(f)])
            mv = tmp
            shuffle(mv)
            pos = choice(mv)
            self.map[pos[0]][pos[1]] = GROUND
            current_pos = vect(pos[0], pos[1])

    def autocreate_map(self):
        ''' Create a labyrinth with the starting point at the top left corner
            and the exit at the opposite corner
        '''
        self.map = [[WALL for _ in range(15)] for _ in range(15)]
        seed()

        # The creation of paths is done between points of coordinates
        # list_pos[i][0] and list_pos[i][1]. This choice is arbitrary.
        list_pos = [
            [[0, 0], [14, 14]],
            [[0, 4], [14, 10]],
            [[0, 10], [14, 4]],
            [[14, 0], [0, 14]],
            [[4, 0], [10, 14]],
            [[10, 0], [4, 14]]
        ]

        # Marking a path for each list_pos element
        for start, end in list_pos:
            self.map[start[0]][start[1]] = GROUND
            self._create_way(start, end)

    def print_map(self):
        ''' Labyrinth display on the console '''
        if not self.map:
            return

        s = "   "
        for r in range(14):
            s = s + "{:2}".format(str(r)) + " "
        s = s + "14"
        print(s)

        num = 0
        for r in self.map:
            s = ""
            s = s + "{:2}[".format(num)
            for c in r[:10]:
                s = s + "{:2}".format(str(c)) + " "
            for c in r[10:14]:
                s = s + "{:2}".format(c) + " "
            s = s + "{:2}]".format(r[-1])
            print(s)
            num += 1


def main():
    laby = Labyrinth()
    laby.autocreate_map()
    laby.print_map()

    nb_wall = 0
    nb_ground = 0
    for r in laby.map:
        for c_r in r:
            if c_r == GROUND:
                nb_ground += 1
            else:
                nb_wall += 1
    print("Number of walls : {}, number of soil elements : {}"
          .format(nb_wall, nb_ground))

    answer = input("Would you like to save the maze in a file [Y]es : ")
    pattern = compile(r"(y$)|yes", IGNORECASE)
    if pattern.match(answer):
        ret = laby.save_map()
        if ret:
            print("saved file")


if __name__ == "__main__":
    main()
