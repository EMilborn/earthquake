import time
import app
import json
from random import randint, choice
import eventlet
import math
from gameinstance import Instance, TICKRATE
import sql
import elo
# from decimal import getcontext, Decimal
# from flask import Flask
# app =
# getcontext().prec = 50

TICKTIME = 1.0 / TICKRATE
REALTICKTIME = float(TICKTIME)  # possibly will be used to account for some time lag


users = {}  # nickname -> real name
lobby = set()
games = {}
usertogame = {}
queueing = set()
running = False


def moveToGame(u1, u2):
    game = Instance(u1, u2)
    gameid = randint(0, 1010101010101010)
    while gameid in games:
        gameid = randint(0, 1010101010101010)
    games[gameid] = game
    usertogame[u1] = gameid
    usertogame[u2] = gameid

def moveToLobby(user):
    usertogame[user] = -1
    lobby.add(user)


def addUser(user, realName):
    users[user] = realName
    moveToLobby(user)
    return user


def leftLobby(user):
    return user in lobby


def usersGame(user):
    if user in usertogame and usertogame[user] != -1:
        return games[usertogame[user]]


def handleEvent(event):
    user = event['user']
    game = usersGame(user)
    if game is not None:
        game.handleEvent(event)

def getState(uid, gameid):
    if uid not in users:
        return -1
    if gameid not in games:
        return 1
    return games[gameid].getGameState()

def updateElo(scores):

    for uid, score in scores.iteritems():
        if score > 4:
            lose = uid
        else:
            win = uid
    winnerId = users[win]
    loserId = users[lose]
    elo.update(winnerId, loserId)
    sql.addWin(winnerId)
    sql.addLoss(loserId)

pops = []
def run():
    global lobby, queueing
    print "Running at", TICKRATE, "Hz"
    running = True
    debugtime = True
    framecount = 0
    lastsecondframe = time.time()
    while(1):
        start = time.time()
        queueingPlayers = lobby & queueing
        while(len(queueingPlayers) > 1):
            p1 = choice(tuple(queueingPlayers))
            queueingPlayers.remove(p1)
            p2 = choice(tuple(queueingPlayers))
            queueingPlayers.remove(p2)
            lobby.remove(p1)
            queueing.remove(p1)
            lobby.remove(p2)
            queueing.remove(p2)
            moveToGame(p1, p2)

        for gid, game in games.iteritems():
            game.gameLoop()
            if game.isOver:
                updateElo(game.scores)
                pops.append(gid)
                for uid, user in game.players.iteritems():
                    moveToLobby(uid)  # right now, the players will be put back in a game with each other lol
        for gid in pops:
            games.pop(gid, None)
        eventlet.sleep(max(0, REALTICKTIME + start - time.time()))
        framecount += 1

# if __name__ == '__main__':
