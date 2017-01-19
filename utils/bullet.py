from tick import TICKMULT

class Bullet:

    DAMAGE = 10
    RADIUS = 5
    DELAY = 30 * TICKMULT
    SPEED = 10 * TICKMULT

    def __init__(self, id, pos, vel):
        self.pos = pos
        self.vel = vel
        self.owner = id

    def update(self):
        self.pos += self.vel

    def collides(self, player):  # xxx add line stuff
        if (self.pos - player.pos).lengthSquared()  \
                <= (self.RADIUS + player.RADIUS) ** 2 \
                and self.owner != player.userid:
            player.health -= self.DAMAGE
            return True
