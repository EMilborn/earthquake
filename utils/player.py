from lagcomp import LagCompClass

class PlayerInput:

    def __init__(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.mouse1 = False
        self.mousePos = None


class Player:

    def __init__(self, id):
        self.pos = Vector(-1, -1)
        self.input = PlayerInput()
        self.userid = id
        self.health = PLAYER_HEALTH
        self.cooldown = 0
        self.lagcomp = LagCompClass()
