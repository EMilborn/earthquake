import os
import glob
import random
from vector import Vector

def dist_sq_line_point(e1, e2, point):  # like project but more efficient
    linevec = e2 - e1
    line_len = linevec.lengthSquared()
    dotNorm = linevec.dot(point - e1) * 1.0 / line_len
    cappedDotNorm = max(0, min(1, dotNorm))
    project = e1 + linevec * cappedDotNorm 
    return (project - point).lengthSquared(), e1 + linevec * dotNorm, dotNorm

class Map:
    def __init__(self, fn=""):
        self.layout = []
        self.vecs = []
        self.spawns = []
        if fn != "":
            self.loadmap(fn)

    def loadmap(self, fn):
        with open(fn, "r") as f:
            map_lines = f.readlines()
        self.layout = [[int(i) for i in s.strip().split(',')] for s in map_lines]
        self.spawns = [Vector(coo[0], coo[1]) for coo in self.layout[:2]]
        self.layout = self.layout[2:]
        self.vecs = [(Vector(coo[0], coo[1]), Vector(coo[2], coo[3])) for coo in self.layout]   


    def __str__(self):
        return str(self.layout)


    def collides(self, pos, vel, r, yOrN=False):  # tests if this map collides with circle at pos + vel, radius r, and says what new vel should be
        rsq = r ** 2
        projectionN = 0
        origvel = vel
        for e1, e2 in self.vecs:
            d, projection, dn = dist_sq_line_point(e1, e2, pos + vel)
            projdir = e2 - e1
            #projection = projdir + e1
            if d < rsq:  # wall collision
                if yOrN:
                    return True
                projectionN += 1
                #  just go to perpendicular to projection on wall, not accurate but only 1 tick
                direction = projdir.rotated90CCW()
                if (pos - e1).isClockwiseOf(projdir):
                    direction = -direction
                newPos = direction.normalized() * r + projection
                vel = newPos - pos
        if yOrN:
            return False
        return vel


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

