import time
from app import send_gamedata
import json
from random import randint
# from flask import Flask
# app =
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

class Instance:
    def __init__(self, user1, user2):
        self.addUser(user1)
        self.addUser(user2)

    def addUser(self, uid):
        print 'adding user ' + uid
        self.players[uid] = Player()
        self.scores[uid] = 0
        self.names[uid] = 'Player ' + str(uid)  # XXX, use sql to get name

    def handleEvent(user, eventType, event):
        if eventType == 'keyboard':
            key = event['key']
            keyDown = event['keyDown']
            if key == 'LeftArrow':
                players[user].input.left = keyDown
            elif key == 'RightArrow':
                players[user].input.right = keyDown
            elif key == 'UpArrow':
                players[user].input.up = keyDown
            elif key == 'DownArrow':
                players[user].input.down = keyDown

    def gameLoop(self):
    for id, user in user:
        if user.input.left:
            user.x -= 1
        if user.input.right:
            user.x += 1
        if user.input.up:
            user.y -= 1
        if user.input.down:
            user.y += 1

    def run(self):
    running = True
    frame = time.time()
    while(1):
        self.gameLoop()
        time.sleep(1/60.)


users = {}
lobby = []
games = {}
usertogame = {}
running = False

def addUser(user):
    print 'adding user'
    lobby.append(user)
    if len(lobby) == 2:
        game = Instance(lobby[0], lobby[1])
        gameid = randint(0, 1928374619283746)
        while gameid in games:
            gameid = randint(0, 1928374619283746)
        games[gameid] = game
        usertogame[lobby[0]] = gameid
        usertogame[lobby[1]] = gameid
        lobby = []

def usersGame(user):
    return games[usertogame[user]]

def handleEvent(user, eventType, event):
    usersGame(user).handleEvent(user, eventType, event)

def getGameState():
    usercoords = []
    for user in users:
        usercoords.append({'x': user.x,'y': user.y})
    return json.dumps(usercoords)

def gameLoop():
    for user in users:
        if user.input.left:
            user.x -= 1
        if user.input.right:
            user.x += 1
        if user.input.up:
            user.y -= 1
        if user.input.down:
            user.y += 1

def run():
    running = True
    frame = time.time()
    while(1):
        gameLoop()
        send_gamedata(getGameState())
        time.sleep(1/60.)

#if __name__ == '__main__':
