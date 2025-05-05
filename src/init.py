from flask import *
from flask_socketio import SocketIO
import logging
import os

app = Flask(__name__, template_folder='../templates')
socketio = SocketIO(app)

def get_logger(name : str, filename : str):
    # Set up raw HTTP logger
    logger = logging.getLogger(name)


    logger.setLevel(logging.INFO)

    # Prevent it from propagating to root logger (i.e.  logfile.log)
    # raw_logger.propagate = False

    # File handler for raw_http.log
    handler = logging.FileHandler(filename)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

    # Add handler to logger
    logger.addHandler(handler)
    return logger

# Set up base HTTP logger
base_logger = get_logger('base_logger', '/mnt/logfile.log')

# Set up base HTTP logger
raw_logger = get_logger('raw_http', '/mnt/raw_http.log')