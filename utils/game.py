import time
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
    def __init__(self):
        self.x = 100
        self.y = 100
        self.input = PlayerInput()

users = []
running = False

def addUser():
    users.append(Player())
    return len(users) - 1

def handleEvent(user, eventType, event):
    print 'in handleEvent'
    if eventType == 'keyboard':
        key = event['key']
        keyDown = event['keyDown']
        if key == 'LeftArrow':
            users[user].input.left = keyDown
        elif key == 'RightArrow':
            users[user].input.right = keyDown
        elif key == 'UpArrow':
            users[user].input.up = keyDown
        elif key == 'DownArrow':
            users[user].input.down = keyDown
        print users[user].input.down, users[user].input.up,users[user].input.left, users[user].input.right

def getGameState():
    usercoords = []
    for user in users:
        usercoords.append((user.x,user.y))
    return usercoords


def gameLoop():
    print 'hai'
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
    print 'hey'
    running = True
    frame = time.time()
    while(1):
        gameLoop()
        time.sleep(1/60.)

#if __name__ == '__main__':