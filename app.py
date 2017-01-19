import eventlet
eventlet.monkey_patch(os=False)
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_socketio import SocketIO, emit
import utils.game
from utils import register as r, sql
import thread
import json
from random import randint
import sqlite3
import os
import sys
f = "data/users.db"
db = sqlite3.connect(f)  # open if f exists, otherwise create
c = db.cursor()

app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)


@app.route("/")
def main():
    if "user" in session:
        return redirect(url_for('home'))
    return redirect(url_for("login", var=" "))


@app.route('/home/')
def home():
    id = utils.game.addUser(session['user'] + str(randint(1, 1000000)))
    return render_template('index.html', id=id)


@socketio.on('message')
def gotmessage(msg):
    print msg, 'from client'


@socketio.on('input')
def handle_input(obj):
    utils.game.handleEvent(obj)


@socketio.on('connect')
def connecter():
    print 'a client connected'
    emit('hello', 'hi client')


@socketio.on('givegame')
def gamegiver(json):
    user = json['user']
    if user in utils.game.usertogame:
        print 'user is in game, sending join'
        emit('join', utils.game.usertogame[json['user']])


@socketio.on('givedata')
def datagiver(json):
    gameid = json['game']
    emit('gamedata', utils.game.games[gameid].getGameState())


@app.route("/login/<var>")
def login(var):
    return render_template("login.html", message=var)


@app.route("/authenticate/", methods=['POST'])
def auth():
    s = r.login(request.form["user"], request.form["password"])
    if s == "Welcome":
        session["user"] = request.form["user"]
        return redirect(url_for('home'))
    return redirect(url_for('login', var=s))


@app.route("/reg/", methods=['POST'])
def reg():
    s = r.regi(request.form["user"], request.form["password"])
    return redirect(url_for('login', var=s))


@app.route("/bye/", methods=['GET', 'POST'])
def bye():
    if "user" in session:
        session.pop("user")
    return redirect(url_for('main'))

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # no buffer
    print 'Starting game thread'
    thread.start_new_thread(utils.game.run, ())
    print 'Started game thread'
    # app.debug = True
    socketio.run(app, host='0.0.0.0')
