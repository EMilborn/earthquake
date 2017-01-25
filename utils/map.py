import os
import glob
import random

class MapTiles:
    WALL = "WALL"
    EMPTY = "EMPTY"
    SPAWN = "SPAWN"
    ERROR = "ERROR"

class Map:
    def __init__(self, fn=""):
        self.layout = [[]]
        if fn != "":
            self.loadmap(fn)
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
        else:
            return MapTiles.ERROR

class MapPicker:
    def __init__(self):
        self.maps = []
        for f in glob.glob("maps/*.map"):
            print f
            self.maps.append(f)
    def get_maps(self):
        return self.maps
    def rand_map(self):
        return random.choice(self.maps)


"""
if __name__ == '__main__':
    mpick = MapPicker()
    print mpick.get_maps()
    print mpick.rand_map()
    mp = Map(mpick.rand_map())
    #mp.loadmap(mpick.rand_map())
    print mp.get()
    print mp.get_at(0,0)
    print mp.get_at(0,1)
    print mp.get_at(1,1)
    mp.display()
"""
