# coding: utf-8


class Graph:
    ''' From a grid representing the accessible areas of the labyrinth, we can
        determine a graph that starts from a certain coordinate of the
        labyrinth and gives all the accessible areas. From then on, we will be
        able to obtain all the possible paths of the graph starting from one
        of its vertices.
    '''
    def __init__(self, map, value):
        ''' Initialization of a grid which indicates the inaccessible squares
            with the value -1 and those which can be traversed by the value 0
            or 1.

            :param map: grid of r lines and c columns unformatted
            :type map: A list containing r lists, each of c items
            :param value: value of a map box indicating that it is accessible
            :type value: int
        '''
        # Graph sought. Each key represents a vertex of the graph. Its
        # associated value will be a list of its closest neighbors in the grid
        self.gph = {}

        self.gd_row = len(map)
        self.gd_col = len(map[0])
        self.grid = []
        for r in range(self.gd_row):
            grid_row = []
            for c in range(self.gd_col):
                grid_row.append(1 if map[r][c] == value else -1)
            self.grid.append(grid_row)

    def _node_adjacent(self, gd, n):
        ''' Returns all nodes adjacent to n that have not already been browsed
            and are accessible in gd
        '''
        up = (n[0] - 1, n[1])  # neighboring node above n
        down = (n[0] + 1, n[1])  # neighboring node below n
        right = (n[0], n[1] + 1)  # neighboring node to the right of n
        left = (n[0], n[1] - 1)  # neighboring node to the left of n

        adj = []  # desired result
        for i, j in [up, down, right, left]:
            # we check that (i, j) are valid coordinates of gd then we check
            # that the node can be traveled and finally we check that the
            # search for a neighbor has not already been done
            if (0 <= i < self.gd_row and 0 <= j < self.gd_col
               and gd[i][j] != -1
               and (i, j) not in self.gph.keys()):
                adj.append((i, j))

        return adj

    def _travel_grid(self, gd, n):
        ''' Path of all elements of the grid gd accessible from node n '''
        gd[n[0]][n[1]] = 0  # indicates that the square has been browsed
        adj = self._node_adjacent(gd, n)  # recovering the adjacent vertices
        # record the link between n and its neighbors in gph
        self.gph[n] = adj
        if adj:
            for a in adj:
                # explore the node a if it has not been seen yet
                if gd[a[0]][a[1]] == 1:
                    self._travel_grid(gd, a)

    def sub_graph(self, node):
        ''' Construct a new graph starting from node "node"

            :param node: starting point (row, column) of the graph
            :type node: tuple
            :return: returns a dictionary whose each key is the coordinate of
                     a vertex of the graph and the value the adjacent vertices
            :rtype: dictionary
        '''
        if self.grid[node[0]][node[1]] == -1:
            return None

        gd = self.grid.copy()  # we are working on a copy of grid
        self.gph = {}  # create a new graph
        self._travel_grid(gd, node)
        return self.gph

    def _next_node(self, way):
        ''' from the path "way", we recover the next nodes of the graph to
            form the other path(s)
        '''
        # the next nodes of the "way" path that extend the gph graph
        nds = self.gph[way[-1]]
        lg = len(nds)
        if lg == 0:  # no node after way[-1]
            return []
        if lg == 1:  # only one node after way[-1]
            way.extend(nds)
            return [way]
        ways = []
        # create as many new paths as there are nodes after way[-1]
        for n in nds:
            w = way.copy()
            w.append(n)
            ways.append(w)
        return ways

    def search_ways(self, node):
        ''' Recherche tous les chemins dans le sous-graph sg en partant de
            node.

            :param sg: graph à parcourir
            :type sg: dictionnaire
            :param node: coordonnées du point d'origine du parcours de sg
            :type node: tuple
            :return: liste contenant tous les chemins. Un chemin est
                     représenté par une liste de sommets dans un tuple
        '''
        if not self.gph or node not in self.gph.keys():
            return []
        ways = [[node]]  # will contain all the paths of the graph
        changed = True  # indicates if a new path is found by true
        while changed:
            changed = False
            for w in ways:  # way of all paths found
                lw = self._next_node(w)
                # if at least one new path is found then we delete the old
                # one and add the new ones to "lw"
                if lw:
                    changed = True
                    ways.remove(w)
                    ways.extend(lw)
        return ways


def main():
    map = [[1, 1, 1, 0, 0],
           [1, 1, 1, 1, 1],
           [0, 1, 1, 0, 1],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0]]

    gph = Graph(map, 1)
    sg = gph.sub_graph((0, 0))
    for k, v in sg.items():
        print(k, ": ", v)
    ways = gph.search_ways((0, 0))
    for w in ways:
        print(w)


if __name__ == '__main__':
    main()
