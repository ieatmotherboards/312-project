from flask import *
from flask_socketio import SocketIO
from src.auth import register_new_account, login, logout
from src.database import users
from src.logging import main_log
import logging
import datetime
from werkzeug.utils import secure_filename
import os
from src.init import app, socketio  # importing app and socketio from src.init instead of declaring here
from src.websockets import connect_websocket  # for some reason this needs to be imported for websockets to work?


logging.basicConfig(filename='logs/record.log', level=logging.INFO, filemode="w") # configure logger in logs file -- must be in logs directory
logging.getLogger('werkzeug').disabled = True # use this to supress automagical werkzeug logs, functional but ugly

UPLOAD_FOLDER = '/public/pfps'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    if "auth_token" not in request.cookies:
        return make_response("Unauthorized", 401)
    

@app.route('/@me')
def at_me():
    if "auth_token" not in request.cookies:
        return make_response("Unauthorized", 401)
    

@app.route('/public/<path:subpath>') # sends files in public directory to client
def send_public_file(subpath):
    try:
        data = get_file("public/" + subpath)
        response = Response(data, mimetype=get_mime_type(subpath))
    except FileNotFoundError:
        response = make_response("Not Found", 404)
    main_log(req=request, res=response)
    return response

@app.route('/phaser-game/<path:subpath>') # sends phaser game files to client
def send_phaser_stuff(subpath):
    try:
        data = get_file("phaser-game/" + subpath)
        response = Response(data, mimetype=get_mime_type(subpath))
    except FileNotFoundError:
        response = make_response("Not Found", 404)
    main_log(req=request, res=response)
    return response

# TODO: should use a library that looks at the bytes of the file
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_pfp', methods = ["POST"])
def upload_pfp():

    # print('request cookies:', request.cookies)
    # app.logger.info("request cookies:%s", str(request.cookies))
    # app.logger.info("request files:%s", str(request.files))

    if 'auth_token' not in request.cookies:
        response = make_response("not logged in", 401)  # 401 = not authorized
    if 'file' not in request.files or request.files['file'] == '':
        response = make_response('bad file', 400) # 400 = bad request
    file = request.files['file']
    if file and is_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response = make_response()
    else:
        response = make_response('', 403) # TODO: what is this error for
    main_log(req=request, res=response)
    return response


    # returns a mime type based on a file's extension
def get_mime_type(path: str):
    split_path = path.split('.')
    filetype = split_path[len(split_path)-1]
    return mime_type[filetype]
# incomplete dict for mime types
mime_type = {
    'js': 'text/javascript',
    'png': 'image/png',
    'css': 'text/css'
}

    # returns a file's contents as bytes
def get_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

if __name__ == '__main__':
    # app.run(debug = False, host='0.0.0.0', port=8000)
    socketio.run(app, debug=False, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
