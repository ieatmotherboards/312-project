from flask import *
from flask_socketio import *
from src.init import app, socketio
import src.database as db

# maps a username to their socket ID
sid_map : dict[str:str] = {}


@socketio.on('connect')
def connect_websocket(socket):
    cookies = request.cookies
    if 'auth_token' in cookies.keys():
        token = cookies['auth_token']
        hashed_token = db.hash_token(token)
        if db.does_hashed_token_exist(hashed_token):
            socket_id = request.sid
            username = db.get_user_by_hashed_token(hashed_token)['username']
            sid_map[socket_id] = username
            emit('connect_echo', {'id': socket_id}, broadcast=False)
            print("connected with " + socket_id)
            return
    print("connected without login")

@socketio.on('player_move')
def player_move(data):
    emit('movement', data, broadcast=True)

@socketio.on('challenge_player')
def challenge_player(data):
    # data: {'challenger': user who initiates, 'defender': user who will be sent the request}
    json_data = json.loads(data)
    defender_username = json_data['defender']
    challenge_data = {'from': json_data['challenger']}
    emit('challenge', challenge_data, to=sid_map[defender_username])

@socketio.on('challenge_response')
def challenge_response(data):
    # data: {'acceptor': user that was sent a challenge, 'challenger': user who initiated the challenge}
    json_data = json.loads(data)
    challenger_username = json_data['challenger']
    challenge_data = {'from': json_data['acceptor']}
    if json_data['accepted']:
        emit('ch_accept', challenge_data, to=sid_map[challenger_username])
    else:
        emit('ch_decline', challenge_data, to=sid_map[challenger_username])


