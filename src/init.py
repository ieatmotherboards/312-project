from flask import *
from flask_socketio import SocketIO
import logging

app = Flask(__name__, template_folder='../templates')
socketio = SocketIO(app)

# Set up raw HTTP logger
raw_logger = logging.getLogger('raw_http')
raw_logger.setLevel(logging.INFO)

# Prevent it from propagating to root logger (i.e.  logfile.log)
raw_logger.propagate = False

# File handler for raw_http.log
raw_handler = logging.FileHandler('raw_http.log')
raw_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Add handler to logger
raw_logger.addHandler(raw_handler)
