from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    return 'this is cool data'

if __name__ == '__main__':
    app.debug = True
    app.run()