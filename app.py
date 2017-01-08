from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import utils.game as game
from thread import start_new_thread
app = Flask(__name__)

@app.route('/')
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
    return jsonify(notjson)

if __name__ == '__main__':
    start_new_thread(game.run, ())
    app.debug = True
    app.run(threaded=True, host='0.0.0.0')
    start_new_thread(game.run, ())
