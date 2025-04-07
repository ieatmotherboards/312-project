'''
To use this: just run main.py in the 312_project server and control click the link that it prints to the console
'''
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/login_data", methods=["POST"])
def parse_data():
    data = request.get_json()
    print("got data")
    js = jsonify({'username': data["username"], "password":data["password"]})
    print(f"got username:{data["username"]} and password:{data["password"]}")
    return js

if __name__ == '__main__':
    app.run(debug = True)

'''
Where to go from here:
    - 
'''