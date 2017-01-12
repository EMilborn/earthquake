import time
import app
import json
from random import randint
# from flask import Flask
# app =
_playerHealth = 100;
_bulletDamage = 10;
_bulletRadius = 5;
_playerRadius = 10;

class PlayerInput:
    def __init__(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.click = False
        self.mousex = -1
        self.mousey = -1

class Player:
    def __init__(self, id):
        self.x = 100
        self.y = 100
        self.input = PlayerInput()
        self.userid = id
        self.health = _playerHealth


class Bullet:
    def __init__(self, id, x, y, xV, yV):
        self.x = x
        self.y = y
        self.xV = xV
        self.yV = yV
        self.owner = id

    def update(self):
        self.x += self.xV
        self.y += self.yV

    def collide(self.player):
        if (player.x ** 2) + (self.x ** 2) < (_bulletRadius + _playerRadius) ** 2 and self.owner != player.userid:
            player.health -= _bulletDamage
            return true
        
class Instance:
    def __init__(self, user1, user2):
        self.players = {}
        self.scores = {}
        self.bullets = {}
        self.addUser(user1)
        self.addUser(user2)

    def addUser(self, uid):
        print 'adding user ' + uid
        self.players[uid] = Player(uid)
        self.scores[uid] = 0
        self.names[uid] = 'Player ' + str(uid)  # XXX, use sql to get name

    def handleEvent(user, eventType, event):
        if eventType == 'keyboard':
            key = event['key']
            keyDown = event['keyDown']
            if key == 'LeftArrow':
                self.players[user].input.left = keyDown
            elif key == 'RightArrow':
                self.players[user].input.right = keyDown
            elif key == 'UpArrow':
                self.players[user].input.up = keyDown
            elif key == 'DownArrow':
                self.players[user].input.down = keyDown

    def gameLoop(self):
        for id, user in self.players.iteritems():
            if user.input.left:
                user.x -= 1
            if user.input.right:
                user.x += 1
            if user.input.up:
                user.y -= 1
            if user.input.down:
                user.y += 1
            #if user.input.click:
            #self.bullets.append(bullet(id, user.x, user.y,

    def getGameState(self):
        usercoords = []
        for id, player in self.players.iteritems():
            usercoords.append({'x': player.x, 'y': player.y})
        return json.dumps(usercoords)


users = {}
lobby = []
games = {}
usertogame = {}
running = False

def addUser(user):
    global lobby
    print 'adding user'
    lobby.append(user)
    print lobby
    if len(lobby) == 2:
        game = Instance(lobby[0], lobby[1])
        gameid = randint(0, 1928374619283746)
        while gameid in games:
            gameid = randint(0, 1928374619283746)
        games[gameid] = game
        usertogame[lobby[0]] = gameid
        usertogame[lobby[1]] = gameid
        lobby = []
    return user

def usersGame(user):
    return games[usertogame[user]]

def handleEvent(user, eventType, event):
    usersGame(user).handleEvent(user, eventType, event)

def run():
    running = True
    frame = time.time()
    while(1):
        # print games
        for id, game in games.iteritems():
            game.gameLoop()
            app.send_gamedata({id: game.getGameState()})
            print(id)
    time.sleep(1/60.)

#if __name__ == '__main__':
