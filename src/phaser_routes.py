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
    return util.log_response(request, response)

@phaser.route('/addCoins', methods=['POST'])
def add_coins():
    data = request.json
    if 'coins' not in data.keys():
        response = make_response('bad data', 400)
        return util.log_response(request, response)
    coins = data['coins']
    # try auth token
    token_attempt = db.try_hash_token(request)
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = make_response(token_attempt[1], token_attempt[2])
        return util.log_response(request, response)

    user = db.get_user_by_hashed_token(hashed_token)
    username=user['username']
    update_coins(username, coins)
    response = make_response()
    return util.log_response(request, response)

@phaser.route('/phaser/playSlots', methods=['POST'])
def slots_request():
    data = request.json
    player_bet = data["bet"]
    # try auth token
    token_attempt = db.try_hash_token(request)
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = make_response(token_attempt[1], token_attempt[2])
        return util.log_response(request, response)

    user = db.get_user_by_hashed_token(hashed_token)
    username=user['username']
    update_coins(username, (-1 * player_bet))
    new_coins : int = get_coins(username)
    if new_coins < 0:
        response = make_response("Not enough coins", 403)
        update_coins(username, (player_bet))
        return util.log_response(request, response)
    result = slots.play_slots(player_bet)
    payout : int = result['payout']
    if payout > 0:
        update_coins(username, payout)
    slots_array = slots_matrix_to_arrays(result['board'])

    response = make_response(json.dumps({'slots': slots_array, 'newCoins': get_coins(username), 'winningLines': result['winning lines']}))
    return util.log_response(request, response)


def slots_matrix_to_arrays(matrix):
    ret = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for y in range(0, 3):
        for x in range(0, 3):
            ret[y][x] = int(matrix[y][x])
    return ret

@phaser.route('/phaser/playRoulette', methods=['POST']) # TODO: finish this
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
        return util.log_response(request, response)
    hashed_token = try_token[0]
    user = db.get_user_by_hashed_token(hashed_token)
    username = user['username']
    wager_data = request.json
    ''' JSON fields are:
    wager
    bet_type
    numbers
    '''
    wager = wager_data['wager']
    bet_type = wager_data['bet_type']
    coins = get_coins(username)
    wager = 1 if wager < 0 else wager
    bet_amount = min(wager, coins) # bet as many coins as user has if they wager more than in inventory

    if bet_type == "Number(s)": # TODO: frontend says Number or Number(s), handle either
        numbers_unparsed = wager_data['numbers']
        numbers = numbers_unparsed.split(', ')
        numbers = [int(num) for num in numbers]
        result = roulette.handlebets([{"name": username, "betAmount": bet_amount, "betType":roulette.find_types(numbers), "numbers":numbers}])
    else:
        result = roulette.handlebets([{"name": username, "betAmount": bet_amount, "betType":bet_type}])
    user_cashout_dict = result[0]
    outcome = result[1]
    base_logger.info(username + " bet on " + bet_type + " and won " + str(user_cashout_dict[username]) + " coins ")
    if user_cashout_dict[username] > 0:
        ach.increment_carousel(username)
    update_coins(username, user_cashout_dict[username])
    wager_data = {"user_cashout": user_cashout_dict[username], "outcome": outcome}
    response = make_response(jsonify(wager_data))
    return util.log_response(request, response)