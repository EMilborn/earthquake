from flask import Flask, render_template, request, session, redirect, url_for
import csv, hashlib, os, sqlite3
from utils import sql

f="data/users.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()

def hash(a):
    return(hashlib.md5(a).hexdigest())

def regi(name, pswrd):
    c = sql.get_all_users()
    if not(name.isalnum()):
        return "Username has bad Characters"
    for user in c:
		if name == user[0]:
			return "Name Taken!"
    sql.add_user(name, hash(pswrd))
    return "User Added"
             

def login(name, pswrd):
    c = sql.get_all_users()
    for user in c:
        if name == user[0]:
            if hash(pswrd) == user[1]:
                return "Welcome"
            return "Incorrect Password"
    return "User Not Found, Please Register"





