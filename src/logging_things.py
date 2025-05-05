import datetime
from flask import request, jsonify, Request, Response, make_response, g
from src.init import app, raw_logger, base_logger
from src.database import get_user_by_hashed_token, hash_token, does_hashed_token_exist


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


TEXT_TYPES = ['application/json', 'text/', 'application/xml', 'application/javascript']

@app.before_request
def capture_request_body():
    # Save request body early; stream will be consumed by Flask handlers
    g.request_body = request.get_data()

@app.after_request
def log_raw_http(response):
    try:
        # Extract request info
        method = request.method
        path = request.path
        headers = dict(request.headers)
        body = g.get('request_body', b'')
        content_type = headers.get('Content-Type', '')

        # Sanitize headers
        if 'Authorization' in headers:
            headers['Authorization'] = '[REDACTED]'
        if 'Cookie' in headers:
            cookies = headers['Cookie'].split(';')
            headers['Cookie'] = '; '.join(
                c if not c.strip().startswith('auth_token=') else 'auth_token=[REDACTED]'
                for c in cookies
            )

        # Determine whether to log body
        log_request_body = (
            all(path_part not in path.lower() for path_part in ['/login', '/register']) and
            any(content_type.startswith(text_type) for text_type in TEXT_TYPES)
        )

        # Prepare request section
        log_entry = f"\n--- REQUEST ---\n{method} {path}\nHeaders: {headers}\n"
        if log_request_body:
            log_entry += f"Body (truncated):\n{body[:2048].decode('utf-8', errors='replace')}\n"
        else:
            log_entry += "Body: [Not Logged]\n"

        # Sanitize response headers
        response_headers = dict(response.headers)
        if 'Set-Cookie' in response_headers:
            set_cookies = response_headers['Set-Cookie'].split(',')
            redacted = ','.join(
                c if 'auth_token=' not in c else '[REDACTED COOKIE]'
                for c in set_cookies
            )
            response_headers['Set-Cookie'] = redacted

        # Determine response body logging
        resp_content_type = response.headers.get('Content-Type', '')
        log_response_body = any(resp_content_type.startswith(text_type) for text_type in TEXT_TYPES)

        # Prepare response section
        log_entry += f"--- RESPONSE ---\nStatus: {response.status}\nHeaders: {response_headers}\n"
        if log_response_body:
            log_entry += f"Body (truncated):\n{response.get_data()[:2048].decode('utf-8', errors='replace')}\n"
        else:
            log_entry += "Body: [Not Logged]\n"

        # Write to log
        raw_logger.info(log_entry)

    except Exception as e:
        raw_logger.error(f"Error while logging raw HTTP: {e}")

    return response


def main_log(req : Request, res : Response): 
    status_code = res.status_code
    if 'auth_token' in req.cookies and req.cookies['auth_token'] != "LOGGED OUT" and does_hashed_token_exist(hashed_token=hash_token(req.cookies['auth_token'])):
        # base_logger.info("auth_token is: " + str(req.cookies['auth_token']))
        username = get_user_by_hashed_token(hash_token(token=req.cookies['auth_token']))['username']
        base_logger.info("\tMETHOD:%s, USERNAME:%s, IP:%s, PATH:%s, TIME:%s, CODE:%s", req.method, username, req.remote_addr, req.path, datetime.datetime.now(), str(status_code))
    else:
        base_logger.info("\tMETHOD:%s, IP:%s, PATH:%s, TIME:%s, CODE:%s", req.method, req.remote_addr, req.path, datetime.datetime.now(), str(status_code))

def auth_log(username : str, success : bool, message : str):
    base_logger.info("\t\tattempt from [%s] to log in, successful?:%s. %s",username, str(success), message)

def logout_log(username: str, success: bool, message: str):
    base_logger.info("\t\tattempt from [%s] to log out, successful?:%s. %s",username, str(success), message)

def register_log(username: str, success: bool, message: str):
    base_logger.info("\t\tattempt from [%s] to register, successful?:%s. %s",username, str(success), message)

def purchase_log(username: str, success: bool, message: str):
    base_logger.info("\t\tattempt from [%s] to purchase, successful?:%s. %s", username, str(success), message)

"""
logging TODO:
    - double check all errors get logged in the stack trace (intentionally break some code (i think this is already done -- thanks flask)) 
    - set up second logfile for full requests/responses
        - add this to volumes
        - should only log first 2048 bytes
        - only log headers for registration, login, and pfp upload requests 
"""