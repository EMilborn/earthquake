from vector import Vector
from player import Player
from bullet import Bullet
from tick import *
import time

class Instance:

    def __init__(self, user1, user2):
        self.players = {}
        self.scores = {}
        self.bullets = []
        self.addUser(user1)
        self.addUser(user2)

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
        
        pass

    def gameLoop(self):
        for uid, user in self.players.iteritems():
            user.lagcomp.remove_old_states()
            user.lagcomp.add_state(user.pos)
            if user.health <= 0:
                self.endGame()
            if user.input.left:
                user.pos.x = max(0, min(800, user.pos.x-1))
            if user.input.right:
                user.pos.x = max(0, min(800, user.pos.x+1))
            if user.input.up:
                user.pos.y = max(0, min(800, user.pos.y-1))
            if user.input.down:
                user.pos.y = max(0, min(800, user.pos.y+1))
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


        for bullet in self.bullets:
            bullet.update()
            for id, user in self.players.iteritems():
                if bullet.collides(user):
                    self.bullets.remove(bullet)

            # if user.input.click:
            # self.bullets.append(bullet(id, user.x, user.y,

    def getGameState(self):
        data = {'users': [], 'bullets': []}
        for uid, player in self.players.iteritems():
            data['users'].append({'x': player.pos.x, 'y': player.pos.y})
        for bullet in self.bullets:
            data['bullets'].append({'x': bullet.pos.x, 'y': bullet.pos.y})
        # print usercoords
        return data
