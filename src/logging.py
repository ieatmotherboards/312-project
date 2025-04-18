import datetime
import flask

def main_log(req:flask.Request, app, code:int): # TODO: make sure we can get IP
    app.logger.info("\tMETHOD:%s, IP:%s, PATH:%s, TIME:%s, CODE:%s", req.method, req.remote_addr, req.path, datetime.datetime.now(), str(code))

def auth_log(username:str, success:bool, message:str, app):
    app.logger.info("attempt from [%s] to login in, successful?:%s. %s",username, str(success), message)
