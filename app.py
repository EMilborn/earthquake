from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import utils.game as game
from thread import start_new_thread
app = Flask(__name__)

@app.route('/')
def home():
    game.addUser('user1')
    return render_template('index.html')

# @app.route('/game', methods=['GET'])
# def rungame():
#     print 'what'
#     if not game.running:
#         game.run()

@app.route('/input', methods=['GET'])
def input():
    print 'is there anybody out there'
    key = request.args.get('key')
    keyDown = request.args.get('state') == 'Down'
    game.handleEvent('user1', 'keyboard', {'key': key, 'keyDown': keyDown})
    return jsonify('')

@app.route('/fetch')
def data():
    x1,y1 = game.getGameState('user1')
    return jsonify('{"x":%d, "y":%d}' % (x1,y1))

if __name__ == '__main__':
    start_new_thread(game.run, ())
    app.debug = True
    app.run(threaded=True)
    start_new_thread(game.run, ())
