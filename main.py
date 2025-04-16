'''
To use this: just run main.py in the 312_project server and control click the link that it prints to the console
'''
from flask import *
from src.auth import register_new_account, parse_data
from src.database import users
from src.logging import main_log
import logging
import datetime
from werkzeug.utils import secure_filename
import os

logging.basicConfig(filename='logs/record.log', level=logging.INFO, filemode="w") # configure logger in logs file -- must be in logs directory
logging.getLogger('werkzeug').disabled = True # use this to supress automatical werkzeug logs, functional but ugly

UPLOAD_FOLDER = '/public/pfps'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/') # this routes to the main page
def home():
    main_log(req=request, app=app, code=200)
    return render_template("index.html")

@app.route('/login') # routes to the login page
def login():
    main_log(req=request, app=app, code=200)
    return render_template("login.html")

@app.route("/login_data", methods=["POST"]) # route for receiving data from login page. calls function in auth.py
def parse_login():
    main_log(req=request, app=app, code=200)
    return parse_data()

@app.route('/register')
def register():
    main_log(req=request, app=app, code=200)
    return render_template("register.html")

@app.route('/register_data', methods = ['POST'])
def register_new():
    main_log(req=request, app=app, code=200)
    return register_new_account()

@app.route('/casino') # routes to the phaser game's page
def render_casino():
    if 'auth_token' not in request.cookies:
        redirect('/', code=302)
    return get_file('phaser-game/game.html')

@app.route('/mines') # routes to the mines page
def render_mines():
    return render_template("mines.html")

@app.route('/settings')
def render_settings():
    main_log(req=request, app=app, code=200)
    return render_template("settings.html")

@app.route('/public/<path:subpath>') # sends files in public directory to client
def send_public_file(subpath):
    data = get_file("public/" + subpath)
    return Response(data, mimetype=get_mime_type(subpath))

@app.route('/phaser-game/<path:subpath>') # sends phaser game files to client
def send_phaser_stuff(subpath):
    data = get_file("phaser-game/" + subpath)
    return Response(data, mimetype=get_mime_type(subpath))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_pfp', methods = ["POST"])
def upload_pfp():

    # print('request cookies:', request.cookies)
    # app.logger.info("request cookies:%s", str(request.cookies))
    # app.logger.info("request files:%s", str(request.files))

    if 'auth_token' not in request.cookies:
        main_log(req=request, app=app, code=302)
        return redirect('/login', code=302)
    if 'file' not in request.files or request.files['file'] == '':
        main_log(req=request, app=app, code=403)
        return Response(status="403")
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    

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
    app.run(debug = False, host='0.0.0.0', port=8000)