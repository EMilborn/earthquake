from lagcomp import LagComp
from vector import Vector
from tick import TICKMULT


class PlayerInput:

    def __init__(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.mouse1 = False
        self.mousePos = None
        self.lockTime = 0  # used for stopping movement at beginning of a round


class Player:

    SPEED = 3 * TICKMULT
    RADIUS = 25
    HEALTH = 100

    def __init__(self, id):
        self.pos = Vector(-1, -1)
        self.input = PlayerInput()
        self.userid = id
        self.health = self.HEALTH
        self.cooldown = 0
        self.lagcomp = LagComp()

    def restartInput(self):
        self.input = PlayerInput()
        self.input.lockTime = 360 * TICKMULT  # 3 second lock
