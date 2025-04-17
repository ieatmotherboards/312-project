'''
To use this: just run main.py in the 312_project server and control click the link that it prints to the console
'''
from flask import *
from flask_socketio import SocketIO
from src.auth import register_new_account, parse_data
from src.database import users
import logging
from src.init import app, socketio  # importing app and socketio from src.init instead of declaring here
from src.websockets import connect_websocket  # for some reason this needs to be imported for websockets to work?


logging.basicConfig(filename='logs/record.log', level=logging.INFO, filemode="w") # configure logger in logs file -- must be in logs directory
logging.getLogger('werkzeug').disabled = True # use this to supress automatical werkzeug logs, functional but ugly

import datetime

@app.route('/') # this routes to the main page
def home():
    app.logger.info("\tMETHOD:%s, IP:%s, PATH:%s, TIME:%s", request.method, request.remote_addr, request.path, datetime.datetime.now()) # tests logger -- works
    return render_template("index.html")

@app.route('/login') # routes to the login page
def login():
    return render_template("login.html")

@app.route("/login_data", methods=["POST"]) # route for receiving data from login page. calls function in auth.py
def parse_login():
    return parse_data()

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_data', methods = ['POST'])
def register_new():
    return register_new_account()

@app.route('/casino') # routes to the phaser game's page
def render_casino():
    return render_template("game.html", path='casino')

@app.route('/mines') # routes to the mines page
def render_mines():
    return render_template("game.html", path='mines')

@app.route('/public/<path:subpath>') # sends files in public directory to client
def send_public_file(subpath):
    data = get_file("public/" + subpath)
    return Response(data, mimetype=get_mime_type(subpath))

@app.route('/phaser-game/<path:subpath>') # sends phaser game files to client
def send_phaser_stuff(subpath):
    data = get_file("phaser-game/" + subpath)
    return Response(data, mimetype=get_mime_type(subpath))

    # returns a mime type based on a file's extension
def get_mime_type(path: str):
    split_path = path.split('.')
    filetype = split_path[len(split_path)-1]
    return mime_type[filetype]
# incomplete dict for mime types
mime_type = {
    'js': 'text/javascript',
    'png': 'image/png',
    'css': 'text/css'
}

    # returns a file's contents as bytes
def get_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

if __name__ == '__main__':
    # app.run(debug = False, host='0.0.0.0', port=8000)
    socketio.run(app, debug=False, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
