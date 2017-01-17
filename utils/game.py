import time
import app
import json
from random import randint
import eventlet
import math
# from flask import Flask
# app =
PLAYER_HEALTH = 100;
PLAYER_SPEED = 3;
PLAYER_RADIUS = 25;

BULLET_DAMAGE = 10;
BULLET_RADIUS = 5;
BULLET_DELAY = 30;
BULLET_SPEED = 6;

class Vector:  # represents 2D vector
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2

    def length(self):
        return math.sqrt(self.lengthSquared())

    def normalized(self):
        l = self.length()
        return Vector(self.x / l, self.y / l)

    def __add__(self, vec2):
        return Vector(self.x + vec2.x, self.y + vec2.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, vec2):
        return self + -vec2

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return self * (1.0 / scalar)

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

class Bullet:
    def __init__(self, id, pos, vel):
        self.pos = pos
        self.vel = vel
        self.owner = id

    def update(self):
        self.pos += self.vel

    def collides(self, player):
        if (self.pos - player.pos).lengthSquared()  \
                <= (BULLET_RADIUS + PLAYER_RADIUS) ** 2 \
                and self.owner != player.userid:
            player.health -= BULLET_DAMAGE
            return True

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

    def gameLoop(self):
        for uid, user in self.players.iteritems():
            if user.input.left:
                user.pos.x -= 1
            if user.input.right:
                user.pos.x += 1
            if user.input.up:
                user.pos.y -= 1
            if user.input.down:
                user.pos.y += 1
            if user.input.mouse1 and not user.input.mousePos is None:
                print 'adding a bullet'
                bulletVel = (user.input.mousePos - user.pos).normalized() * BULLET_SPEED
                newBullet = Bullet(uid, user.pos, bulletVel)
                self.bullets.append(newBullet)
        for bullet in self.bullets:
            bullet.update()
            #if user.input.click:
            #self.bullets.append(bullet(id, user.x, user.y,

    def getGameState(self):
        data = {'users': [], 'bullets': []}
        for uid, player in self.players.iteritems():
            data['users'].append({'x': player.pos.x, 'y': player.pos.y})
        for bullet in self.bullets:
            data['bullets'].append({'x': bullet.pos.x, 'y': bullet.pos.y})
        # print usercoords
        return data


users = {}
lobby = []
games = {}
usertogame = {}
running = False

def addUser(user):
    global lobby
    print 'adding user to lobby'
    lobby.append(user)
    if len(lobby) == 2:
        game = Instance(lobby[0], lobby[1])
        gameid = randint(0, 1928374619283746)
        while gameid in games:
            gameid = randint(0, 1928374619283746)
        games[gameid] = game
        usertogame[lobby[0]] = gameid
        usertogame[lobby[1]] = gameid
        # app.send_joinlobby(lobby[0], gameid)
        # app.send_joinlobby(lobby[1], gameid)
        lobby = []
    return user

def leftLobby(user):
    return user in lobby

def usersGame(user):
    return games[usertogame[user]]

def handleEvent(event):
    user = event['user']
    usersGame(user).handleEvent(event)

def run():
    running = True
    frame = time.time()
    while(1):
        # print games
        for gid, game in games.iteritems():
            game.gameLoop()
            # print(id)
        eventlet.sleep(1/60.)
        # time.sleep(1/60.)

#if __name__ == '__main__':
