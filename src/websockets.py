from flask import *
from flask_socketio import *
from src.init import app, socketio

# websockets = Blueprint('websockets', __name__)
        # blueprints can be used to modularize normal flask stuff, but not websockets

@socketio.on('connect')
def connect_websocket():
    cookies = request.cookies
    if 'auth_token' in cookies.keys():
        print("connected with " + cookies['auth_token'])
    else:
        print("connected without login")
    emit('connect_echo')

@socketio.on('player_move')
def player_move(data):
    emit('movement', data, broadcast=True)
