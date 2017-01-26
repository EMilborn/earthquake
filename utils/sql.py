import sqlite3
import csv

f = "data/users.db"


def db_f(func):
    def wrapped(*args, **kwargs):  # handles locking and weird db issues
        try:
            if isinstance(args[0], sqlite3.Connection):  # db is in args
                return func(*args, **kwargs)
        except IndexError:
            pass
        db = sqlite3.connect(f)
        v = func(db, *args, **kwargs)
        db.close()
        return v
    return wrapped


@db_f
def init(db):
    cur = db.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT, rating FLOAT, wins INTEGER, losses INTEGER)")
    cur.execute("INSERT INTO users VALUES (-1, '', '', 1500.0, 0, 0)")
    db.commit()


@db_f
def add_user(db, user, password):
    cur = db.cursor()
    q = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)"

    cur.execute(q, (next_userid(db), user, password, 1500.0, 0, 0))
    db.commit()


@db_f
def get_userid(db, user):
    id_holder = db.cursor().execute(
        'SELECT id FROM users WHERE username = ?', (user,))
    for row in id_holder:
        return row[0]


@db_f
def get_all_users(db):
    cur = db.cursor()
    res = cur.execute("SELECT * FROM users")
    L = []
    for row in res:
        L += [[row[1], row[2]]]
    return L


@db_f
def next_userid(db):
    uids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM users')]
    return max(uids) + 1

@db_f
def getRating(db, username):
    cur = db.cursor()
    res = cur.execute("SELECT rating FROM users WHERE username = ?", (username,))
    for i in res:
        return i[0]

@db_f
def setRating(db, username, rating):
    cur = db.cursor()
    old = getRating(db, username)
    cur.execute("UPDATE users SET rating=? WHERE username = ?", (rating, username))
    db.commit()
    return old

@db_f
def getRecord(db, username):
    cur = db.cursor()
    res = cur.execute("SELECT wins, losses FROM users WHERE username = ?", (username,))
    for i in res:
        return i

@db_f
def addWin(db, username):
    wins = getRecord(db, username)[0]

    cur = db.cursor()
    cur.execute("UPDATE users SET wins=? WHERE username = ?", (wins + 1, username))
    db.commit()
    return wins

@db_f
def addLoss(db, username):
    losses = getRecord(db, username)[1]
    cur = db.cursor()
    cur.execute("UPDATE users SET losses=? WHERE username = ?", (losses + 1, username))
    db.commit()
    return losses
