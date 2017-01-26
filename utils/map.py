import os
import glob
import random


class Map:
    def __init__(self, fn=""):
        self.layout = []
        if fn != "":
            self.loadmap(fn)
    def loadmap(self, fn):
        with open(fn, "r") as f:
            map_lines = f.readlines()
        self.layout = [[int(i) for i in s.strip().split(',')] for s in map_lines]
    def __str__(self):
        return str(self.layout)


class MapPicker:
    def __init__(self):
        self.maps = []
        for f in glob.glob("maps/*.map"):
            print f
            self.maps.append(f)

    def rand_map(self):
        return Map(random.choice(self.maps))



if __name__ == '__main__':
    mpick = MapPicker()
    print mpick.get_maps()
    mp = Map(mpick.rand_map())
    print mp

