from utils import sql
import sqlite3
k = 8.0

f = "data/users.db"
db = sqlite3.connect(f)

def update(uW, uL):
    rW = sql.getRating(db, uW)
    rL = sql.getRating(db, uL)
    odds = 1/(1 + 10**((rL - rW)/400))##ELO STUFF
    delta = k(1.0 - odds)
    sql.setRating(db, uW, rW + delta)
    sql.setRating(db, uL, rL + delta)
    
