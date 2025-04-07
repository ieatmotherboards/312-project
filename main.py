'''
To use this: just run main.py in the 312_project server and control click the link that it prints to the console
'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True)

'''
Where to go from here:
    - 
'''