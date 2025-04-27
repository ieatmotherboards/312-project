# packages
from flask import *
from flask_socketio import SocketIO
import logging
import datetime
from werkzeug.utils import secure_filename
import os
import uuid

# our code
from src.init import app, socketio  # importing app and socketio from src.init instead of declaring here
from src.auth import register_new_account, login, logout
import src.database as db
from src.logging import main_log
import src.util as util

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
    logout_result = logout(request=request)
    if logout_result[0] == 200:
        response = make_response("Logout Success", 200)
        response.set_cookie('auth_token', 'logged out', max_age=0, httponly=True)
    else:
        response = make_response(logout_result[1], logout_result[0]) # update this to take other text later
    main_log(req=request, res=response)
    return response

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
        response = redirect('/', code=302)  # TODO: should change to a 400-level response and display an alert on frontend
    else:
        response = make_response(render_template("game.html", path='casino/mainCasino.js'))
    main_log(req=request, res=response)
    return response

@app.route('/roulette')
def render_roulette():
    if 'auth_token' not in request.cookies:
        response = redirect('/', code=302)  # TODO: should change to a 400-level response and display an alert on frontend
        return response
    
    js_path = 'casino/scenes/Roulette.js'

    response = make_response(render_template("game.html", path=js_path))
    main_log(req=request, res=response)
    return response

@app.route('/mines') # routes to the mines page
def render_mines():
    response = make_response(render_template("game.html", path='mines/mainMines.js'))
    main_log(req=request, res=response)
    return response

@app.route('/settings')
def render_settings():
    response = make_response(render_template("settings.html"))
    main_log(req=request, res=response)
    return response

@app.route('/@me')
def at_me():
    """
        Args:
            None. Just make a frontend fetch call to this endpoint.
        Returns:
            - 401 response if not logged in OR
            - JSON response in format {"username":[USERNAME]}
    """
    token_attempt = db.try_hash_token(request)
    hashed_token = token_attempt[0]
    if hashed_token is None:
        response = make_response(token_attempt[1], token_attempt[2])
        main_log(req=request, res=response)
        return response
    username = db.get_user_by_hashed_token(hashed_token)['username']
    data = {"username":username}
    response = make_response(jsonify(data))
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

        new_filename = str(uuid.uuid4()) + "." + file.filename.split(".")[1]
        filename = secure_filename(new_filename)

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.info("Saving to: " + upload_path)
        file.save(upload_path)
        db.users.update_one({"username":username},{"$set":{"pfp":new_filename}}) #TODO: pass in correct path
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
        return jsonify({"path":'public/pfps/'+filename})
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