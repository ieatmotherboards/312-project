from flask import *
from src.logging_things import main_log

def send_file_response(path):
    try:
        data = get_file(path)
        response = Response(data, mimetype=get_mime_type(path))
    except FileNotFoundError:
        response = make_response("Not Found", 404)
    return response

    # returns a mime type based on a file's extension
def get_mime_type(path: str):
    split_path = path.split('.')
    filetype = split_path[len(split_path)-1].lower()
    return mime_type[filetype]
# incomplete dict for mime types
mime_type = {
    'js': 'text/javascript',
    'png': 'image/png',
    'css': 'text/css',
    'ico':'image/x-icon',
    'jpg':'image/jpeg',
    'jpeg':'image/jpeg',
    'gif':'image/gif',
}

    # returns a file's contents as bytes
def get_file(filename):
    with open(filename, 'rb') as file:
        return file.read()
    
def take_away_token_response(request: Request, token_attempt):
    response = make_response(token_attempt[1], token_attempt[2])
    response.set_cookie('auth_token', 'InvalidAuth', max_age=0, httponly=True)
    return response

def log_response(request : Request, response: Response):
    main_log(request, response)
    return response