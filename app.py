from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import utils.game as game

app = Flask(__name__)

@app.route('/')
def home():
    game.addUser('user1')
    return render_template('index.html')

@app.route('/input', methods=['GET'])
def input():
    key = request.args.get('key')
    game.handleEvent('user1', key)
    return jsonify('')

@app.route('/fetch')
def data():
    x1,y1 = game.getGameState('user1')
    return jsonify('{"x":%d, "y":%d}' % (x1,y1))

if __name__ == '__main__':
    app.debug = True
    app.run()
