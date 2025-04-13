'''
To use this: just run main.py in the 312_project server and control click the link that it prints to the console
'''
from flask import Flask, render_template, request
from auth import parse_data

import logging

logging.basicConfig(filename='record.log', level=logging.INFO, filemode="w") # initializes logger 

app = Flask(__name__)

@app.route('/') # this routes to the main page
def home():
    return render_template("index.html")

@app.route('/login') # routes to the login page
def login():
    return render_template("login.html")

@app.route("/login_data", methods=["POST"]) # route for receiving data from login page. calls function in auth.py
def parse_login():
    return parse_data()

@app.route('/casino') # routes to the casino page
def render_casino():
    return render_template("casino.html")

@app.route('/mines') # routes to the mines page
def render_mines():
    return render_template("mines.html")

if __name__ == '__main__':
    app.run(debug = True)