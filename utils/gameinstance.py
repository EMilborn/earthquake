from vector import Vector
from player import Player
from bullet import Bullet
from tick import *

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
            if user.health <= 0:
                self.endGame()
            if user.input.left:
                user.pos.x -= 1
            if user.input.right:
                user.pos.x += 1
            if user.input.up:
                user.pos.y -= 1
            if user.input.down:
                user.pos.y += 1
            user.cooldown -= 1
            if user.input.mouse1 and user.cooldown < 0:
                print 'adding a bullet'
                #client_state = user.lagcomp.get_approx_client_state()
                #print "bt time:", client_state[0]
                #pos = client_state[1]
                #mousePos = client_state[2]
                pos = user.pos
                mousePos = user.input.mousePos
                if mousePos:
                    bulletVel = (mousePos-pos).normalized() * Bullet.SPEED
                    newBullet = Bullet(uid, pos, bulletVel)
                    self.bullets.append(newBullet)
                    user.cooldown = Bullet.DELAY

            user.lagcomp.remove_old_states()
            user.lagcomp.add_state(user.pos, user.input.mousePos)

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
