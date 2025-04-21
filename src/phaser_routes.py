from flask import *
import src.database as db
import src.util as util
from src.logging import main_log

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
        user = db.get_user_by_hashed_token(hashed_token)
        if user is None:
            response = make_response('Invalid auth token', 403)
        else:
            response = make_response({
                'coins': user['coins']
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
    if 'auth_token' not in request.cookies.keys():
        response = make_response('not logged in', 403)
        main_log(req=request, res=response)
        return response
    hashed_token = db.hash_token(request.cookies['auth_token'])
    user = db.get_user_by_hashed_token(hashed_token)
    if user is None:
        response = make_response('invalid auth token', 403)
        main_log(req=request, res=response)
        return response
    new_coins = coins + user["coins"]
    db.users.update_one({"auth_token": hashed_token}, {"$set": {"coins": new_coins}})
    response = make_response()
    main_log(req=request, res=response)
    return response