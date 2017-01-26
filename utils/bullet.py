from tick import TICKMULT

class Bullet:

    DAMAGE = 20
    RADIUS = 10
    DELAY = 60 * TICKMULT
    SPEED = min(10 * TICKMULT, RADIUS * 2 - 0.1)  # has to be < radius*2 for collision

    def __init__(self, id, pos, vel):
        self.pos = pos
        self.vel = vel
        self.owner = id

    def update(self):
        self.pos += self.vel

    def collides(self, player):
        if (self.pos - player.pos).lengthSquared()  \
                <= (self.RADIUS + player.RADIUS) ** 2 \
                and self.owner != player.userid:
            return True
