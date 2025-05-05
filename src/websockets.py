from flask import *
from flask_socketio import *
from src.init import app, socketio
import src.database as db
import src.games.coin_flip as coin
import src.inventory as inv
import src.achievements as ach

# maps a username to their socket ID
sid_map : dict[str:str] = {}

user_dc_queue : dict[str, list[str]] = {}

@socketio.on('connect')
def connect_websocket(socket):
    cookies = request.cookies
    if 'auth_token' in cookies.keys():
        token = cookies['auth_token']
        hashed_token = db.hash_token(token)
        if db.does_hashed_token_exist(hashed_token):
            socket_id = request.sid
            username = db.get_user_by_hashed_token(hashed_token)['username']
            sid_map[username] = socket_id
            emit('connect_echo', {'id': socket_id}, broadcast=False)
            if not username in user_dc_queue.keys():
                user_dc_queue[username] = []
            return
    print("connected without login")

@socketio.on('disconnect')
def disconnect_websocket(socket):
    cookies = request.cookies
    if 'auth_token' in cookies.keys():
        token = cookies['auth_token']
        hashed_token = db.hash_token(token)
        if db.does_hashed_token_exist(hashed_token):
            socket_id = request.sid
            username = db.get_user_by_hashed_token(hashed_token)['username']
            next_in_queue = user_dc_queue[username].pop(0)
            app.logger.info("user was connected to " + next_in_queue)
            if next_in_queue == 'casino' and username in casino_users.keys():
                casino_users.pop(username)
                emit('casino_leave', {'username': username}, broadcast=True)
            elif next_in_queue == 'coin' and username in coinflip_instances.keys():
                emit('opponent_disconnect', {'opponent': username}, to=sid_map[coinflip_instances[username]])
                coinflip_instances.pop(username)
            return
    print("disconnected without login")

casino_users = {}

def update_user_pos(data : dict[str, dict[str, int]]):
    username = data['username']
    position = data['pos']
    casino_users[username] = {'x': position['x'], 'y': position['y']}

@socketio.on('casino_join')
def casino_join(data):
    update_user_pos(data)
    emit('movement', data, broadcast=True)
    socket_id = sid_map[data['username']]
    user_dc_queue[data['username']].append('casino')
    for player in casino_users:
        emit('movement', {'username': player, 'pos': casino_users[player]}, to=socket_id)

@socketio.on('casino_leave')
def casino_leave(data):
    username = data['username']
    casino_users.pop(username)
    emit('casino_leave', data, broadcast=True)

@socketio.on('player_move')
def player_move(data):
    update_user_pos(data)
    emit('movement', data, broadcast=True)

@socketio.on('challenge_player')
def challenge_player(data):
    # data: {'challenger': user who initiates, 'defender': user who will be sent the request}
    defender_username = data['defender']
    challenge_data = {'from': data['challenger']}
    emit('challenge', challenge_data, to=sid_map[defender_username])

coinflip_instances = {}

@socketio.on('challenge_response')
def challenge_response(data):
    # data: {'acceptor': user that was sent a challenge, 'challenger': user who initiated the challenge}
    challenger_username = data['challenger']
    acceptor_username = data['acceptor']
    challenge_data = {'from': acceptor_username}
    if data['accepted']:
        emit('ch_accept', challenge_data, to=sid_map[challenger_username])
        coinflip_instances[challenger_username] = acceptor_username
        coinflip_instances[acceptor_username] = challenger_username
        user_dc_queue[challenger_username].append('coin')
        user_dc_queue[acceptor_username].append('coin')
    else:
        emit('ch_decline', challenge_data, to=sid_map[challenger_username])

# TODO: add consent
@socketio.on("flip_coin")
def flip_coin(data):
    # data = {'to': user they are competing with, 'from': user in question}
    sending_user = data['from']
    receiving_user = data['to']
    result = coin.coinflip()
    if result:
        ach.increment_flipper(sending_user)
        inv.update_coins(sending_user, 1)
        inv.update_coins(receiving_user, -1)
    else:
        ach.increment_flipper(receiving_user)
        inv.update_coins(sending_user, -1)
        inv.update_coins(receiving_user, 1)
    result_data = {sending_user: inv.get_coins(sending_user), receiving_user: inv.get_coins(receiving_user), 'result': result}
    emit('flip_result', result_data, to=sid_map[sending_user])
    emit('flip_result', result_data, to=sid_map[receiving_user])

@socketio.on('get_coins')
def get_coins_ws(data):
    username = data['username']
    result_data = {'username': username, 'coins': inv.get_coins(username)}
    emit('coins', result_data, to=request.sid)

@socketio.on('get_opponent')
def get_opponent(data):
    username = data['username']
    opponent_data = {'opponent': coinflip_instances[username]}
    emit('opponent', opponent_data, to=request.sid)