'''
To use this: just run main.py in the 312_project server and control click the link that it prints to the console
'''
from flask import *
from src.auth import register_new_account, parse_data
from src.database import users
import logging

logging.basicConfig(filename='record.log', level=logging.INFO, filemode="w") # initializes logger 

app = Flask(__name__)

@app.route('/') # this routes to the main page
def home():
    # test database
    users.insert_one({"IP":request.remote_addr}) # tests database by inserting IP addr of user when loading main page
    return render_template("index.html")

@app.route('/login') # routes to the login page
def login():
    return render_template("login.html")

@app.route("/login_data", methods=["POST"]) # route for receiving data from login page. calls function in auth.py
def parse_login():
    return parse_data()

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_data', methods = ['POST'])
def register_new():
    return register_new_account()

@app.route('/casino') # routes to the phaser game's page
def render_casino():
    return get_file('phaser-game/game.html')

@app.route('/mines') # routes to the mines page
def render_mines():
    return render_template("mines.html")

@app.route('/public/<path:subpath>') # sends files in public directory to client
def send_public_file(subpath):
    data = get_file("public/" + subpath)
    return Response(data, mimetype=get_mime_type(subpath))

@app.route('/phaser-game/<path:subpath>') # sends phaser game files to client
def send_phaser_stuff(subpath):
    data = get_file("phaser-game/" + subpath)
    return Response(data, mimetype=get_mime_type(subpath))


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
    app.run(debug = True, host='0.0.0.0', port=8000)