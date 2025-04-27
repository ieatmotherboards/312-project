import datetime
from flask import request, jsonify, Request, Response, make_response
from src.init import app
from src.database import get_user_by_hashed_token, hash_token


@app.errorhandler(404)
def not_found_error(error):
    response = make_response("Page Not Found", 404)
    # You can call your custom logger here
    main_log(request, response)
    return response

@app.errorhandler(500)
def internal_error(error):
    response = make_response("Internal Server Error", 500)
    # You can call your custom logger here
    main_log(request, response)
    return response


def main_log(req : Request, res : Response): 
    status_code = res.status_code
    if 'auth_token' in req.cookies and req.cookies['auth_token'] != "LOGGED OUT":
        app.logger.info("auth_token is: " + str(req.cookies['auth_token']))
        username = get_user_by_hashed_token(hash_token(token=req.cookies['auth_token']))['username']
        app.logger.info("\tMETHOD:%s, USERNAME:%s, IP:%s, PATH:%s, TIME:%s, CODE:%s", req.method, username, req.remote_addr, req.path, datetime.datetime.now(), str(status_code))
    else:
        app.logger.info("\tMETHOD:%s, IP:%s, PATH:%s, TIME:%s, CODE:%s", req.method, req.remote_addr, req.path, datetime.datetime.now(), str(status_code))

def auth_log(username : str, success : bool, message : str):
    app.logger.info("\t\tattempt from [%s] to log in, successful?:%s. %s",username, str(success), message)

def logout_log(username: str, success: bool, message: str):
    app.logger.info("\t\tattempt from [%s] to log out, successful?:%s. %s",username, str(success), message)

def register_log(username: str, success: bool, message: str):
    app.logger.info("\t\tattempt from [%s] to register, successful?:%s. %s",username, str(success), message)

"""
logging TODO:
    - double check all errors get logged in the stack trace (intentionally break some code (i think this is already done -- thanks flask)) 
    - set up second logfile for full requests/responses
        - add this to volumes
        - should only log first 2048 bytes
        - only log headers for registration, login, and pfp upload requests 
"""