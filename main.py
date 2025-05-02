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
from src.inventory import purchase_loot_box, getLeaderBoard
from src.logging_things import main_log
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
    main_log(req=request, res=response)
    return response

@app.route('/login') # routes to the login page
def render_login():
    response = make_response(render_template("login.html"))
    main_log(req=request, res=response)
    return response

@app.route("/login_data", methods=["POST"]) # route for receiving data from login page. calls function in auth.py
def parse_login():
    login_result = login(request)
    if 'auth_token' in login_result:
        cookie = login_result['auth_token']
        response = make_response()
        response.set_cookie('auth_token', cookie, max_age=86400, httponly=True)
    else:
        response = make_response(login_result['error'], 403)
    main_log(req=request, res=response)
    return response
    
@app.route('/logout_data', methods=['POST'])
def parse_logout():
    main_log(req=request, res=make_response("OK", 200))
    logout_result = logout(request=request)
    # if logout_result[0] == 200:

    # else:
    #     response = make_response(logout_result[1], logout_result[0]) # update this to take other text later
    return logout_result

@app.route('/register')
def register():
    response = make_response(render_template("register.html"))
    main_log(req=request, res=response)
    return response

@app.route('/register_data', methods = ['POST'])
def register_new():
    response = register_new_account(request)
    main_log(req=request, res=response)
    return response

@app.route('/casino') # routes to the phaser game's page
def render_casino():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
    else:
        response = make_response(render_template("game.html", path='casino/mainCasino.js'))
    main_log(req=request, res=response)
    return response

@app.route('/roulette')
def render_roulette():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
        return response

    js_path = 'casino/scenes/Roulette.js'

    response = make_response(render_template("game.html", path=js_path))
    main_log(req=request, res=response)
    return response

@app.route('/settings')
def render_settings():
    response = make_response(render_template("settings.html"))
    main_log(req=request, res=response)
    return response

@app.route('/open-lootbox') # routes to the login page
def render_lootbox():
    response = make_response(render_template("open_lootbox.html"))
    main_log(req=request, res=response)
    return response

@app.route('/open-lootbox', methods = ['POST']) # routes to the login page
def open_lootbox():
    response = purchase_loot_box(request)
    main_log(req=request, res=response)
    return response

@app.route('/item-shop') # routes to the login page
def render_shop():
    response = make_response(render_template("item_shop.html"))
    main_log(req=request, res=response)
    return response

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
        response = make_response(token_attempt[1], token_attempt[2])
        response.set_cookie('auth_token', 'InvalidAuth', max_age=0, httponly=True)
        main_log(req=request, res=response)
        return response
    user = db.get_user_by_hashed_token(hashed_token)
    username = user['username']
    coins = inv.get_coins(username)
    pfp = user['pfp']
    data = {"username": username, "coins": coins, "pfp_path": pfp}
    response = make_response(jsonify(data))
    main_log(req=request, res=response)
    return response

@app.route('/leaderboard')
def render_leaderboard():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)
    else:
        response = make_response(render_template("leaderboard.html"))
    main_log(req=request, res=response)
    return response

@app.route('/leaderboard', methods = ['POST'])
def send_leaderboard_data():
    sorted = getLeaderBoard()
    response = make_response(jsonify({"leaderboard": sorted}))
    main_log(req=request, res=response)
    return response

@app.route('/@user/<path:subpath>') # sends files in public directory to client
def at_user(subpath):
    user : dict = db.get_user_by_username(subpath)
    if user is None:
        response = make_response("user does not exist", 404)
    else:
        response = make_response({ "pfp_path": user["pfp"], "coins": inv.get_coins(subpath) })
    main_log(req=request, res=response)
    return response

@app.route('/public/<path:subpath>') # sends files in public directory to client
def send_public_file(subpath):
    response = util.send_file_response("public/" + subpath)
    main_log(req=request, res=response)
    return response

# TODO: should use a library that looks at the bytes of the file
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
        res = make_response("not logged in", 401)  # 401 = not authorized
        main_log(req=request,res=res)
        return res
    elif 'file' not in request.files or request.files['file'] == '':
        res = make_response('bad file', 400) # 400 = bad request
        main_log(req=request,res=res)
        return res

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
        res = make_response("OK", 200)
        main_log(req=request, res=res)
        return res

    res = make_response("Bad Request",400)
    main_log(req=request, res=res)
    return res

@app.route('/get_pfp')
def get_pfp():
    if 'auth_token' not in request.cookies:
        res = make_response("not logged in", 401)  # 401 = not authorized
        main_log(req=request,res=res)
        return res

    # TODO: get file path and pass in as param to send_public_file
    hashed_token = db.hash_token(request.cookies['auth_token'])
    user = db.get_user_by_hashed_token(hashed_token=hashed_token)
    if "pfp" in user:
        filename = user["pfp"]
        main_log(req=request, res=make_response("OK",200))
        return jsonify({"path": filename})
    else:
        res = make_response("Profile picture not found", 400) # no pfp found
        main_log(req=request, res=res)
        return res

# returns a file's contents as bytes
def get_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)