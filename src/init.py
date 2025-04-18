from flask import *
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='../templates')
socketio = SocketIO(app)