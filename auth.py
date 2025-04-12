from flask import Flask, render_template, request, jsonify

def parse_data():
    data = request.get_json()
    print("got data")
    js = jsonify({'username': data["username"], "password":data["password"]})
    print(f"got username:{data["username"]} and password:{data["password"]}")
    return js