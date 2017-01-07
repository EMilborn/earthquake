class Player:
    def __init__(self):
        self.x = 100
        self.y = 100

users = {}

def addUser(username):
    users[username] = Player()

def handleEvent(user, key):
    if key == 'LeftArrow':
        users[user].x -= 10
    elif key == 'RightArrow':
        users[user].x += 10
    elif key == 'UpArrow':
        users[user].y -= 10
    elif key == 'DownArrow':
        users[user].y += 10

def getGameState(user):
    if user in users:
        return users[user].x,users[user].y
    return 0,0
