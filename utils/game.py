import time
import app
import json
from random import randint
import eventlet
import math
from lagcomp import LagCompClass
from vector import Vector
from player import Player
from bullet import Bullet
from gameinstance import Instance, TICKRATE
# from decimal import getcontext, Decimal
# from flask import Flask
# app =
# getcontext().prec = 50

TICKTIME = 1.0 / TICKRATE
REALTICKTIME = float(TICKTIME)  # possibly will be used to account for some time lag


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
    print "Running at", TICKRATE, "Hz"
    running = True
    debugtime = True
    framecount = 0
    lastsecondframe = time.time()
    while(1):
        start = time.time()
        for gid, game in games.iteritems():
            game.gameLoop()
        eventlet.sleep(max(0, REALTICKTIME + start - time.time()))
        framecount += 1

# if __name__ == '__main__':
