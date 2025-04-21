import datetime
import flask
from src.init import app

def main_log(req : flask.Request, res : flask.Response): # TODO: make sure we can get IP
    status_code = res.status_code
    app.logger.info("\tMETHOD:%s, IP:%s, PATH:%s, TIME:%s, CODE:%s", req.method, req.remote_addr, req.path, datetime.datetime.now(), str(status_code))

def auth_log(username : str, success : bool, message : str):
    app.logger.info("\t\tattempt from [%s] to log in, successful?:%s. %s",username, str(success), message)

def logout_log(username: str, success: bool, message: str):
    app.logger.info("\t\tattempt from [%s] to log out, successful?:%s. %s",username, str(success), message)

def register_log(username: str, success: bool, message: str):
    app.logger.info("\t\tattempt from [%s] to log out, successful?:%s. %s",username, str(success), message)