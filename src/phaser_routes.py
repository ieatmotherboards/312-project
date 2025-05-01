from flask import *
import src.database as db
import src.util as util
from src.logging_things import main_log
from src.inventory import get_coins, update_coins
import src.games.slots as slots
import src.games.roulette as roulette
import src.achievements as ach
from src.init import app

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
            username = user['username']
            response = make_response({
                'coins': get_coins(username),
                'username': username
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
    update_coins(username, coins)
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
    update_coins(username, (-1 * player_bet))
    new_coins : int = get_coins(username) - player_bet
    if new_coins < 0:
        response = make_response("Not enough coins", 403)
        main_log(req=request, res=response)
        return response
    result = slots.play_slots(player_bet)
    payout : int = result['payout']
    if payout > 0:
        update_coins(username, payout)
    slots_array = slots_matrix_to_arrays(result['board'])

    response = make_response(json.dumps({'slots': slots_array, 'newCoins': get_coins(username)}))
    main_log(req=request, res=response)
    return response


def slots_matrix_to_arrays(matrix):
    ret = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for y in range(0, 3):
        for x in range(0, 3):
            ret[y][x] = int(matrix[y][x])
    return ret

@phaser.route('/phaser/playRoulette',methods=['POST']) # TODO: finish this
def roulette_request():
    """
    Args: None. uses JSON from POST request

    Returns:
        - response with JSON in the format:
            "user_cashout" : int representing the coins won,
            "outcome" : int representing the winning number
        - also edits coin amount in user DB
    """
    try_token = db.try_hash_token(request=request)
    if try_token[0] is None:
        response = make_response(try_token[1], try_token[2])
        main_log(req=request, res=response)
        return response

    user = db.get_user_by_hashed_token(try_token[0])
    username = user['username']
    data = request.json
    ''' JSON fields are:
    wager
    bet_type
    numbers
    '''

    wager = data['wager']
    bet_type = data['bet_type']
    coins = get_coins(username)
    app.logger.info("to start, user has " + str(coins) + " coins.")
    wager = 1 if wager < 0 else wager
    bet_amount = min(wager, coins) # bet as many coins as user has if they wager more than in invetory
    # app.logger.info("Wager amount: " + str(bet_amount))
    # app.logger.info("bet_type: " + bet_type)
    # app.logger.info("username: " + username)

    if bet_type == "Number(s)": # TODO: frontend says Number or Number(s), handle either
        numbers_unparsed = data['numbers']
        numbers = numbers_unparsed.split(', ')
        # app.logger.info("numbers are:", numbers)
        numbers = [int(num) for num in numbers]
        result = roulette.handlebets([{"name": username, "betAmount": bet_amount, "betType":roulette.find_types(numbers), "numbers":numbers}])
        # update user coins on backend
        

    else:
        result = roulette.handlebets([{"name": username, "betAmount": bet_amount, "betType":bet_type}])

    user_cashout_dict = result[0]
    outcome = result[1]
    app.logger.info("user " + username + " bet on " + bet_type + " and won/lost " + str(user_cashout_dict[username]) + " coins ")
    app.logger.info("they now have "+ str(coins + user_cashout_dict[username]))
    # db.invetory.find_one_and_update({"username":username}, {"$set":{"coins":coins + user_cashout_dict[username]}}) # TODO: math
    if user_cashout_dict[username] >0:
        ach.increment_carousel(username)
    update_coins(username=username, coin_change=user_cashout_dict[username])
    data = {"user_cashout": user_cashout_dict[username], "outcome": outcome}
    res = make_response(jsonify(data))
    main_log(req=request, res=res)

    return res