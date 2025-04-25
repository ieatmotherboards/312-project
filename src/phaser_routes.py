from flask import *
import src.database as db
import src.util as util
from src.logging import main_log
import src.games.slots as slots
from src.inventory import getCoins, updateCoins

# passed into main.py to register routes
phaser = Blueprint('phaser_routes', __name__)

# routes relating to phaser games

@phaser.route('/phaser-game/<path:subpath>') # sends phaser game files to client
def send_phaser_file(subpath):
    response = util.send_file_response("phaser-game/" + subpath)
    main_log(req=request, res=response)
    return response

@phaser.route('/phaser/@me')
def phaser_me():
    if 'auth_token' in request.cookies:
        hashed_token = db.hash_token(request.cookies['auth_token'])
        username = db.get_user_by_hashed_token(hashed_token)['username']
        if username is None:
            response = make_response('Invalid auth token', 403)
        else:
            response = make_response({
                'coins': getCoins(username)
            })
    else:
        response = make_response('Not logged in', 403)
    main_log(req=request, res=response)
    return response

@phaser.route('/addCoins', methods=['POST'])
def add_coins():
    data = request.json
    
    if 'coins' not in data.keys():
        response = make_response('bad data', 400)
        main_log(req=request, res=response)
        return response
    coins = data['coins']
    # try auth token
    token_attempt = db.try_hash_token(request)
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = make_response(token_attempt[1], token_attempt[2])
        main_log(req=request, res=response)
        return response

    user = db.get_user_by_hashed_token(hashed_token)
    username=user['username']
    updateCoins(username,coins)
    response = make_response()
    main_log(req=request, res=response)
    return response

@phaser.route('/phaser/playSlots', methods=['POST'])
def slots_request():
    data = request.json
    player_bet = data["bet"]
    # try auth token
    token_attempt = db.try_hash_token(request)
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = make_response(token_attempt[1], token_attempt[2])
        main_log(req=request, res=response)
        return response

    user = db.get_user_by_hashed_token(hashed_token)
    username=user['username']
    updateCoins(username,(-1*player_bet))
    new_coins : int = getCoins(username) - player_bet
    if new_coins < 0:
        response = make_response("Not enough coins", 403)
        main_log(req=request, res=response)
        return response
    result = slots.play_slots(player_bet)
    payout : int = result['payout']
    if payout > 0:
        updateCoins(username,payout)
    slots_array = slots_matrix_to_arrays(result['board'])
    
    response = make_response(json.dumps({'slots': slots_array, 'newCoins': getCoins(username)}))
    main_log(req=request, res=response)
    return response


def slots_matrix_to_arrays(matrix):
    ret = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for y in range(0, 3):
        for x in range(0, 3):
            ret[y][x] = int(matrix[y][x])
    return ret