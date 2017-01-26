import os
import glob
import random
from vector import Vector

def dist_line_point(e1, e2, point):
    linevec = e2 - e1
    line_len = linevec.lengthSquared()
    dotNorm = max(0, min(1, linevec.dot(point - e1) / line_len))
    project = e1 + linevec * dotNorm 
    return (project - point).length()

class Map:
    def __init__(self, fn=""):
        self.layout = []
        self.vecs = []
        if fn != "":
            self.loadmap(fn)

    def loadmap(self, fn):
        with open(fn, "r") as f:
            map_lines = f.readlines()
        self.layout = [[int(i) for i in s.strip().split(',')] for s in map_lines]
        self.vecs = [(Vector(coo[0], coo[1]), Vector(coo[2], coo[3])) for coo in self.layout]   
    def __str__(self):
        return str(self.layout)



    def collides(self, pos, r):  # tests if this map collides with circle at pos, radius r
        for e1, e2 in self.vecs:
            d = dist(e1, e2, pos)
            if d < r:
                return True
        return False


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

