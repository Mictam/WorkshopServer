from flask import Flask
from flask import jsonify, request, redirect
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/add_move",  methods=["POST"])
def add_move():
    if not request.json:
        return "Account data not provided", 400

