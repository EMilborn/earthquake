class MapTiles:
    WALL = "WALL"
    EMPTY = "EMPTY"
    SPAWN = "SPAWN"

class Map:
    def __init__(self):
        self.layout = [[]]
    def loadmap(self, fn):
        with open(fn, "r") as f:
            map_lines = f.readlines()
        self.layout = [s.strip() for s in map_lines]
    def display(self):
        for r in self.layout:
            print r
    def get(self):
        return self.layout
    def get_at(self, i, j):
        c = self.layout[i][j]
        if c == '+':
            return MapTiles.WALL
        if c == ' ':
            return MapTiles.EMPTY
        if c == 'o':
            return MapTiles.SPAWN

"""
if __name__ == '__main__':
    mp = Map()
    mp.loadmap("test.map")
    print mp.get_at(1,1)
    print mp.get_at(1,2)
    mp.display()
"""
