from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import utils.game as game
from utils import register as r, sql
from thread import start_new_thread
import os, sqlite3
import json

f="data/users.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route("/")
def main():
    if "user" in session:
        return redirect(url_for('home'))
    return redirect(url_for("login", var =" "))

@app.route('/home/')
def home():
    id = game.addUser()
    return render_template('index.html', id=id)

# @app.route('/game', methods=['GET'])
# def rungame():
#     print 'what'
#     if not game.running:
#         game.run()

@app.route('/input', methods=['GET'])
def input():
    key = request.args.get('key')
    keyDown = request.args.get('state') == 'Down'
    uid = request.args.get('user')
    game.handleEvent(int(uid), 'keyboard', {'key': key, 'keyDown': keyDown})
    return jsonify('')

@app.route('/fetch', methods=['GET'])
def data():
    users = game.getGameState()
    notjson = []
    for coo in users:
        notjson.append({'x': coo[0], 'y': coo[1]})
    return json.dumps(notjson)

@app.route("/login/<var>")
def login(var):
    return render_template("login.html", message = var)

@app.route("/authenticate/", methods = ['POST'])
def auth():
    s = r.login(request.form["user"],request.form["password"])
    if s == "Welcome":
        session["user"] = request.form["user"]
        return redirect(url_for('home'))
    return redirect(url_for('login', var = s))

@app.route("/reg/", methods = ['POST'])
def reg():
    s = r.regi(request.form["user"],request.form["password"])
    return redirect(url_for('login', var = s))

@app.route("/bye/", methods = ['GET','POST'])
def bye():
    if "user" in session:
        session.pop("user")
    return redirect(url_for('main'))

if __name__ == '__main__':
    start_new_thread(game.run, ())
    app.debug = True
    app.run(threaded=True, host='0.0.0.0')
    start_new_thread(game.run, ())
