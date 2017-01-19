class Bullet:

    def __init__(self, id, pos, vel):
        self.pos = pos
        self.vel = vel
        self.owner = id

    def update(self):
        self.pos += self.vel

    def collides(self, player):  # xxx add line stuff
        if (self.pos - player.pos).lengthSquared()  \
                <= (BULLET_RADIUS + PLAYER_RADIUS) ** 2 \
                and self.owner != player.userid:
            player.health -= BULLET_DAMAGE
            return True
