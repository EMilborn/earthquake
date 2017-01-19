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
    cur.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT, rating INTEGER)")
    cur.execute("INSERT INTO users VALUES (-1, '', '', 1500)")
    db.commit()


@db_f
def add_user(db, user, password):
    cur = db.cursor()
    q = "INSERT INTO users VALUES (%d, \'%s\', \'%s\')" % (
        next_userid(db), user, password, 1500)
    print q
    cur.execute(q)
    db.commit()


@db_f
def get_userid(db, user):
    id_holder = db.cursor().execute(
        'SELECT id FROM users WHERE username = "' + user + '"')
    L = []
    for row in id_holder:
        return row[0]


@db_f
def get_all_users(db):
    cur = db.cursor()
    res = cur.execute("SELECT * FROM users")
    L = []
    for row in res:
        L += [[row[1], row[2]]]
    db.commit()
    return L


@db_f
def next_userid(db):
    uids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM users')]
    return max(uids) + 1


try:
    init()
except:
    pass
