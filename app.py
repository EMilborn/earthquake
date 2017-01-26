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
import time

app = Flask(__name__)
app.secret_key = 'xtrem c-cret kee'
socketio = SocketIO(app)


@app.route("/")
def main():
    if "user" in session:
        return redirect(url_for('home'))
    return redirect(url_for("login", var=" "))


@app.route('/home/')
def home():
    id = utils.game.addUser(session['user'] + str(randint(1, 1000000)), session['user'])
    return render_template('index.html', id=id, name=session['user'])
		
@app.route('/player/')
def player():
		user = session['user']
                rec = sql.getRecord(user)
                rat = sql.getRating(user)
		return render_template('player.html', user = user, win = rec[0], loss = rec[1], rating = rat )


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
    if user in utils.game.usertogame and utils.game.usertogame[user] != -1:
        gid = utils.game.usertogame[user]
        gMap = utils.game.games[gid].myMap
        players = utils.game.games[gid].players.keys()
        realnames = {}
        for uid in players:
            realnames[uid] = utils.game.users[uid]
        print 'user is in game, sending join'
        emit('join', {'gid': gid, 'map': gMap.layout, 'names': realnames})


@socketio.on('givedata')
def datagiver(json):
    gameid = json['game']
    uid = json['user']
    emit('gamedata', utils.game.getState(uid, gameid))


@socketio.on('ping')
def ping(json):
    user = json['user']
    gameid = json['game']
    if gameid == -1 or gameid not in utils.game.games:
        return
    utils.game.games[gameid].players[user].lastPing = time.time()
    emit('pong')

@socketio.on('ping2')
def ping2(json):
    user = json['user']
    gameid = json['game']
    if gameid == -1:
        return
    dT = time.time() - utils.game.games[gameid].players[user].lastPing
    utils.game.games[gameid].players[user].lagcomp.add_latency(dT)


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
    f = "data/users.db"
    if not os.path.exists(f) or os.path.getsize(f) == 0:
        db = sqlite3.connect(f)
        sql.init(db)
        db.close()

    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # no buffer
    print 'Starting game thread'
    thread.start_new_thread(utils.game.run, ())
    print 'Started game thread'
    app.debug = sys.platform != 'win32'
    socketio.run(app, host='0.0.0.0')
