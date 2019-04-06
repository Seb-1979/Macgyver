# coding: utf-8


class Graph:
    def __init__(self, map, value):
        ''' Initialisation d'une grille qui indique les cases inaccessibles
            avec la valeur -1 et celles qui peuvent être parcourues par la
            valeur 1.

            :param map: la grille non formatée
            :type map: r listes de listes de longueur c
            :param value: valeur d'une case de map indiquant qu'elle est
                          accessible
            :type value: type acceptant la comparaison "==" entre les éléments
                         de map et value
        '''
        self.gd_row = len(map)
        self.gd_col = len(map[0])
        self.grid = []
        for r in range(self.gd_row):
            grid_row = []
            for c in range(self.gd_col):
                grid_row.append(1 if map[r][c] == value else -1)
            self.grid.append(grid_row)

    # retourne tous les noeuds adjacents à n
    def _node_adjacent(self, sg, gd, n):
        up = (n[0] - 1, n[1])  # noeud voisin de n en haut
        down = (n[0] + 1, n[1])  # noeud voisin de n en bas
        right = (n[0], n[1] + 1)  # noeud voisin de n à droite
        left = (n[0], n[1] - 1)  # noeud voisin de n à gauche

        adj = []
        for i, j in [up, down, right, left]:
            # on vérifie que (i, j) sont des coordonnées valides de gd
            if (0 <= i < self.gd_row and 0 <= j < self.gd_col
               # on vérifie que le noeud peut-être parcouru
               and gd[i][j] != -1
               # on vérifie que la recherche de voisin n'a pas déjà été
               # effectuée
               and (i, j) not in sg.keys()):
                adj.append((i, j))

        return adj

    def _travel_grid(self, sg, gd, n):
        gd[n[0]][n[1]] = 0 # indique que la case a été parcourue
        adj = self._node_adjacent(sg, gd, n)  # sommets adjacent
        sg[n] = adj
        if adj:
            for a in adj:
                # parcours le noeud s'il n'a pas encore été vu
                if gd[a[0]][a[1]] == 1:
                    self._travel_grid(sg, gd, a)

    def sub_graph(self, node):
        ''' Construit un nouveau graph partant

            :param node: point (ligne, colonne) de départ du graph
            :type node: tuple
            :return: retoure un dictionnaire dont chaque clé est la coordonnée
                     d'un somment du graph et la valeur les sommets adjacents
            :rtype: dictionnaire
        '''
        if self.grid[node[0]][node[1]] == -1:
            return None

        gd = self.grid.copy()
        # valeur 0 donnée dans la grille quand le noeud a déjà été parcouru
        sg = {}  # graph recherché
        self._travel_grid(sg, gd, node)
        return sg
    
    def _next_node(self, sg, node, node_seen):
        node_seen.append(node)
        adj = sg[node]
        for a in adj:
            if a not in adj:
                return _next_node(sg, a, node_seen)
        return node_seen

    def search_way(self, sg, node):
        ''' Recherche tous les chemins dans le sous-graph sg en partant de
            node.
            
            :param sg: graph à parcourir
            :type sg: dictionnaire
            :param node: coordonnées du point d'origine du parcours de sg
            :type node: tuple
            :return: liste contenant tous les chemins. Un chemin est
                     représenté par une liste de sommets dans un tuple
        '''
        if node not in sg.keys():
            return []
        way = []
        node_seen = [node]
        way.append(self._next_node(sg, node, node_seen))


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
#    gph.search_way(sg, (0, 0))

if __name__ == '__main__':
    main()
