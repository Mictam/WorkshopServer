from flask import Flask
from flask import jsonify, request, redirect
from Queue.queue import __Queue

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/add_move", methods=["GET"])
def add_move(Q = __Queue):
    if "id" not in request.args:
        return "Move ID not provided in request", 400
    id = request.args.get('id')
    __Queue.add_to_queue(Q, id)
    print(Q.get_queue(Q))
    return  "success", 200






