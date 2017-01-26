from vector import Vector
from player import Player
from bullet import Bullet
from tick import *
import elo
import time
import sql
from map import MapPicker


LEFT = Vector(-Player.SPEED, 0)
UP = Vector(0, -Player.SPEED)
RIGHT = Vector(Player.SPEED, 0)
DOWN = Vector(0, Player.SPEED)


class Instance:

    def __init__(self, user1, user2):
        self.players = {}
        self.scores = {}
        self.bullets = []
        self.addUser(user1)
        self.addUser(user2)
        self.isOver = False
        self.spawnPlayers()
        self.myMap = MapPicker().rand_map()


    def addUser(self, uid):
        print 'adding user to game'
        self.players[uid] = Player(uid)
        self.scores[uid] = 0

    def handleEvent(self, event):
        etype = event['event']
        uid = event['user']
        user = self.players[uid]
        if etype == 'key':
            key = event['key']
            keyDown = event['state']
            if key == 'LeftArrow':
                user.input.left = keyDown
            elif key == 'RightArrow':
                user.input.right = keyDown
            elif key == 'UpArrow':
                user.input.up = keyDown
            elif key == 'DownArrow':
                user.input.down = keyDown
            elif key == 'Mouse1':
                user.input.mouse1 = keyDown
        if etype == 'mousemove':
            if user.input.mousePos is None:
                user.input.mousePos = Vector(0, 0)
            user.input.mousePos.x = event['x']
            user.input.mousePos.y = event['y']

    def endGame(self):
        self.isOver = True

    def spawnPlayers(self):
        first = 0
        for uid, user in self.players.iteritems():
            user.pos = Vector(first * 500 + 100, first * 500 + 100)
            user.restartInput()
            user.health = Player.HEALTH
            first += 1
        self.bullets = []  # kill current bullets

    def gameLoop(self):
        for uid, user in self.players.iteritems():
            user.lagcomp.remove_old_states()
            user.lagcomp.add_state(user.pos)
            if user.health <= 0:
                self.scores[uid] += 1
                if self.scores[uid] > 4:  # this player loses
                    self.endGame()
                    return
                else:
                    self.spawnPlayers()
            if user.input.lockTime <= 0:
                velocity = Vector(0,0)
                if user.input.left:
                    velocity += LEFT
                if user.input.right:
                    velocity += RIGHT
                if user.input.up:
                    velocity += UP
                if user.input.down:
                    velocity += DOWN
                velocity = self.myMap.collides(user.pos, velocity, Player.RADIUS)
                user.pos += velocity
                user.cooldown -= 1
                if user.input.mouse1 and user.cooldown < 0:
                    client_state = user.lagcomp.get_approx_client_state()
                    if client_state != -1:
                        pos = client_state[1]
                    else:
                        pos = user.pos
                    mousePos = user.input.mousePos
                    if mousePos:
                        bulletVel = (mousePos-pos).normalized() * Bullet.SPEED
                        newBullet = Bullet(uid, pos, bulletVel)
                        self.bullets.append(newBullet)
                        user.cooldown = Bullet.DELAY
            else:
                user.input.lockTime -= 1


        for bullet in self.bullets:
            bullet.update()
            for id, user in self.players.iteritems():
                if bullet.collides(user):
                    self.bullets.remove(bullet)
                    user.health -= Bullet.DAMAGE
                    continue
            if self.myMap.collides(bullet.pos, Vector(0,0), Bullet.RADIUS, True):
                self.bullets.remove(bullet)


            # if user.input.click:
            # self.bullets.append(bullet(id, user.x, user.y,

    def getGameState(self):
        if self.isOver:
            return {'end': True}
        data = {'users': {}, 'bullets': []}
        for uid, player in self.players.iteritems():
            data['users'][uid] = {'x': player.pos.x, 'y': player.pos.y}
        for bullet in self.bullets:
            data['bullets'].append({'x': bullet.pos.x, 'y': bullet.pos.y})
        # print usercoords
        return data
