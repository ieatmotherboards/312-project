from flask import Flask, request, jsonify

def parse_data():
    '''
    dummy function to pull out username and password from frontend, replace this with actual logic later
    to see how this works on the frontend, check out sendData() in login.html
    '''
    data = request.get_json()
    print("got data")
    js = jsonify({'username': data["username"], "password":data["password"]})
    print(f"got username:{data["username"]} and password:{data["password"]}")
    return js