from flask import *
from flask_socketio import *
from src.init import app, socketio
import src.database as db
import secrets

# websockets = Blueprint('websockets', __name__)
        # blueprints can be used to modularize normal flask stuff, but not websockets

@socketio.on('connect')
def connect_websocket():
    cookies = request.cookies
    if 'auth_token' in cookies.keys():
        token = cookies['auth_token']
        hashed_token = db.hash_token(token)
        if db.does_hashed_token_exist(hashed_token):
            socket_id = secrets.token_hex()
            emit('connect_echo', {'id': socket_id})
            print("connected with " + socket_id)
            return
    print("connected without login")


@socketio.on('player_move')
def player_move(data):
    emit('movement', data, broadcast=True)
