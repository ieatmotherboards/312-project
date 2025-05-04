# packages
from flask import *
from flask_socketio import SocketIO
import logging
import datetime
from werkzeug.utils import secure_filename
import os
import uuid
from PIL import Image

# our code
from src.init import app, socketio  # importing app and socketio from src.init instead of declaring here
from src.auth import register_new_account, login, logout
import src.database as db
from src.inventory import purchase_loot_box, getLeaderBoard, list_inventory, get_item_properties, getCoinsAndLootBoxCount, trade
from src.logging_things import main_log
from src.achievements import generate_html_data
import src.util as util
import src.inventory as inv

# routes & websockets
from src.websockets import connect_websocket  # for some reason this needs to be imported for websockets to work
from src.phaser_routes import phaser


logging.basicConfig(filename='/mnt/logfile.log', level=logging.INFO, filemode="w")
logging.getLogger('werkzeug').disabled = True # use this to supress automatic werkzeug logs (which are free game but super cluttered)

UPLOAD_FOLDER =  os.path.join(os.getcwd(), 'public', 'pfps')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(phaser)

@app.route('/') # this routes to the main page
def home():
    response = make_response(render_template("index.html"))
    return util.log_response(request, response)

@app.route('/login') # routes to the login page
def render_login():
    response = make_response(render_template("login.html"))
    return util.log_response(request, response)

@app.route("/login_data", methods=["POST"]) # route for receiving data from login page. calls function in auth.py
def parse_login():
    login_result = login(request)
    if 'auth_token' in login_result:
        cookie = login_result['auth_token']
        response = make_response()
        response.set_cookie('auth_token', cookie, max_age=86400, httponly=True)
    else:
        response = make_response(login_result['error'], 403)
    return util.log_response(request, response)
    
@app.route('/logout_data', methods=['POST'])
def parse_logout():
    logout_response = logout(request)
    return util.log_response(request, logout_response)

@app.route('/register')
def register():
    response = make_response(render_template("register.html"))
    return util.log_response(request, response)

@app.route('/register_data', methods = ['POST'])
def register_new():
    response = register_new_account(request)
    return util.log_response(request, response)

@app.route('/casino') # routes to the phaser game's page
def render_casino():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
    else:
        response = make_response(render_template("game.html", path='casino/mainCasino.js'))
    return util.log_response(request, response)

@app.route('/roulette')
def render_roulette():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
    else:
        response = make_response(render_template("game.html", path='roulette/mainRoulette.js'))
    return util.log_response(request, response)

@app.route('/settings')
def render_settings():
    response = make_response(render_template("settings.html"))
    return util.log_response(request, response)

@app.route('/open-lootbox') # routes to the open box page
def render_lootbox():
    response = make_response(render_template("open_lootbox.html"))
    return util.log_response(request, response)

@app.route('/item-shop', methods = ['POST']) # POST to try to buy item
def open_lootbox():
    response = purchase_loot_box(request)
    return util.log_response(request, response)

@app.route('/item-shop') # routes to the shop page
def render_shop():
    response = make_response(render_template("item_shop.html"))
    return util.log_response(request, response)

@app.route('/@me')
def at_me():
    """
        Args:
            None. Just make a frontend fetch call to this endpoint.
        Returns:
            - 401 response if not logged in OR
            - JSON response in format {"username": username, "coins": user's current coins, "pfp_path": path to pfp}
    """
    token_attempt = db.try_hash_token(request) # TODO: if auth token isn't recognized, send back a token to clear it
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = util.take_away_token_response(request, token_attempt)
        return util.log_response(request, response)
    user = db.get_user_by_hashed_token(hashed_token)
    username = user['username']
    coins = inv.get_coins(username)
    data = {"username": username, "coins": coins}
    if 'pfp' in user.keys():
        data['pfp_path'] = user['pfp']
    response = make_response(jsonify(data))
    return util.log_response(request, response)

@app.route('/leaderboard')
def render_leaderboard():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
    else:
        response = make_response(render_template("leaderboard.html"))
    return util.log_response(request, response)

@app.route('/leaderboard', methods = ['POST'])
def send_leaderboard_data():
    leaderboard = getLeaderBoard()
    response = make_response(jsonify({"leaderboard": leaderboard}))
    return util.log_response(request, response)

@app.route('/@user/<path:subpath>') # sends files in public directory to client
def at_user(subpath):
    user : dict = db.get_user_by_username(subpath)
    if user is None:
        response = make_response("user does not exist", 404)
    else:
        response = make_response({ "pfp_path": user["pfp"], "coins": inv.get_coins(subpath) })
    return util.log_response(request, response)

@app.route('/inventory')
def render_inventory():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
    else:
        response = make_response(render_template("inventory.html"))
    return util.log_response(request, response)

@app.route('/get-inventory', methods = ['POST'])
def send_inventory_data():
    
    potential_json = request.get_json() # double check that this doesn't error
    if potential_json is None:
        if 'auth_token' not in request.cookies:
            response = redirect('/', code=302)
            return util.log_response(request, response)
        token_attempt = db.try_hash_token(request)
        hashed_token = token_attempt[0]
        if hashed_token is None:
            response = util.take_away_token_response(request, token_attempt)
            return util.log_response(request, response)
        username = db.get_user_by_hashed_token(hashed_token)['username']
    else:
        username = potential_json['username']

        
    inventory = list_inventory(username)
    out_list = []
    for item in inventory:
        properties = get_item_properties(item['id'])
        out_list.append({"id": item['id'], "name": properties['name'], "image": properties['imagePath']})
        # app.logger.info("item is: " + str(item))
    return util.log_response(request, make_response(jsonify(out_list)))

@app.route('/get-trade-users', methods=['POST'])
def get_trade_users():

    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302) 
        main_log(req=request, res=response)
        return response
    
    token_attempt = db.try_hash_token(request) 
    hashed_token = token_attempt[0]
    if hashed_token is None:
        return util.take_away_token_response(request, token_attempt)
    
    username = db.get_user_by_hashed_token(hashed_token)['username']

    search_term = request.get_json()['search']
    app.logger.info('received search term: ' + str(search_term))
    # users_list = db.find_trade_list(search_term)

    users_list = db.users.find({}).to_list()

    out_list = []
     # take out own username
    for user in users_list:
        found_username = user['username']
        # app.logger.info("found user with name" + str(found_username))
        if found_username != username and found_username.lower() in search_term.lower():
            out_list.append(found_username)
    # app.logger.info("returning:" +str(out_list))
    return util.log_response(request, make_response(jsonify(out_list)))

@app.route('/request-trade', methods = ['POST'])
def request_trade():
    '''
    JSON:
    target_username: targetUsername,
    your_item_id: yourItem.id,
    their_item_id: theirItem.id
    '''

    # get username from auth token for the 80th time
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
        return util.log_response(request, response)
    token_attempt = db.try_hash_token(request)
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = util.take_away_token_response(request, token_attempt)
        return util.log_response(request, response)
    
    username = db.get_user_by_hashed_token(hashed_token=hashed_token)

    request_json = request.get_json()
    requesting_username = username
    responding_username = request_json['target_username']

    your_item_id = request_json['your_item_id']
    your_image_path = get_item_properties(your_item_id)['imagePath']

    their_item_id = request_json['their_item_id']
    their_image_path = get_item_properties(their_item_id)['imagePath']

    tradeId = str(uuid.uuid4) # TODO: see if necessary 
    db.trades.insert_one({"tradeId":tradeId, 
                          "requesting_username": requesting_username, 
                          "responding_username": responding_username, 
                          "requesting_id": your_item_id, 
                          "responding_id": their_item_id,
                          "requesting_item_imagepath": your_image_path,
                          "responding_item_imagepath": their_image_path
                          })
    response = make_response("OK", 200)
    return util.log_response(request, response)

@app.route('/respond-to-trade', methods = ['POST'])
def respond_trade():
    the_json = request.get_json()
    accept_status = True if the_json['response'] == 'accept' else False
    if accept_status:
        found_trade = db.trades.find_one({"tradeId": the_json['trade_id']})
        # user1_stuff & user2_stuff = {'coins': coins to lose, 'items': list of items to lose}

        requesting_stuff = {"coins": 0, "items": [found_trade["requesting_id"]]}
        responding_stuff = {"coins": 0, "items": [found_trade["responding_id"]]}
        trade(user1=found_trade["requesting_username"], 
              user1_stuff=requesting_stuff, 
              user2=found_trade["responding_username"],
              user2_stuff=responding_stuff)
        return util.log_response(request, make_response("OK", 200))
    else:
        return util.log_response(request, make_response("OK", 200))

@app.route('/get-pending-trades')
def get_pending_trades():
    # get user by auth token
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
        return util.log_response(request, response)
    token_attempt = db.try_hash_token(request)
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = util.take_away_token_response(request, token_attempt)
        return util.log_response(request, response)
    
    username = db.get_user_by_hashed_token(hashed_token=hashed_token)
    
    # query db for trades involving that user's items
    trades = db.trades.find({"responding_username":username}).to_list()

    out_list = []
    out_list.append({'tradeId':trade['tradeId'], 
                     'requesting_username':trade['requesting_username'], 
                     'responding_username': trade['responding_username'],
                     'requesting_item_imagepath':trade['requesting_item_imagepath'],
                     'responding_item_imagepath': trade['responding_item_imagepath']} for trade in trades)
    return util.log_response(request, jsonify(out_list))

@app.route('/public/<path:subpath>') # sends files in public directory to client
def send_public_file(subpath):
    response = util.send_file_response("public/" + subpath)
    return util.log_response(request, response)

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_pfp', methods = ["POST"])
def upload_pfp():
    """
    Args:
        None. Just make a fetch request of method "POST" to this endpoint.
    Returns:
        - 401 if not logged in OR
        - 400 if file isn't properly formatted OR
        - 200 OK and saves file in public/pfps if valid and updates user db entry to have 'pfp' field mapping to file path
    """

    if 'auth_token' not in request.cookies:
        response = make_response("not logged in", 401)  # 401 = not authorized
        return util.log_response(request, response)
    elif 'file' not in request.files or request.files['file'] == '':
        response = make_response('bad file', 400) # 400 = bad request
        return util.log_response(request, response)

    token = db.hash_token(request.cookies['auth_token'])
    username = db.get_user_by_hashed_token(token)["username"]

    file = request.files['file']
    if file and is_allowed_file(file.filename):
        new_filename = str(uuid.uuid4()) + '.png'
        filename = secure_filename(new_filename)

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.info("Saving to: " + upload_path)
        image = Image.open(file)
        size = image.size
        if size[0] < size[1]:
            size = size[0]
        else:
            size = size[1]
        image = image.crop((0, 0, size, size))
        image = image.resize((64, 64))
        image.save(upload_path)
        db.users.update_one({"username":username},{"$set":{"pfp": "public/pfps/"+new_filename}}) #TODO: pass in correct path
        response = make_response()
        return util.log_response(request, response)

    response = make_response("Bad Request",400)
    return util.log_response(request, response)

@app.route('/get_pfp')
def get_pfp():
    if 'auth_token' not in request.cookies:
        response = make_response("not logged in", 401)  # 401 = not authorized
        return util.log_response(request, response)

    # TODO: get file path and pass in as param to send_public_file
    hashed_token = db.hash_token(request.cookies['auth_token'])
    user = db.get_user_by_hashed_token(hashed_token=hashed_token)
    if "pfp" in user:
        filename = user["pfp"]
        response = make_response(jsonify({"path": filename}))
        return util.log_response(request, response)
    else:
        response = make_response("Profile picture not found", 400) # no pfp found
        return util.log_response(request, response)

@app.route('/achievements')
def achievements():
    # Fetch the achievement data for the user
    token_attempt = db.try_hash_token(request) # TODO: if auth token isn't recognized, send back a token to clear it
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = make_response(token_attempt[1], token_attempt[2])
        response.set_cookie('auth_token', 'InvalidAuth', max_age=0, httponly=True)
        return util.log_response(request, response)
    username = db.get_user_by_hashed_token(hashed_token)['username']
    data = generate_html_data(username)
    response = make_response(render_template('achievements.html', username=username, achievements=data))
    return util.log_response(request, response)

@app.route('/player_stats')
def playerStats():
    token_attempt = db.try_hash_token(request) # TODO: if auth token isn't recognized, send back a token to clear it
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = make_response(token_attempt[1], token_attempt[2])
        response.set_cookie('auth_token', 'InvalidAuth', max_age=0, httponly=True)
        return util.log_response(request, response)
    username = db.get_user_by_hashed_token(hashed_token)['username']
    data = getCoinsAndLootBoxCount(username)
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json'
    return util.log_response(request, response)


# returns a file's contents as bytes
def get_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)