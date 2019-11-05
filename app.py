from flask import Flask
from flask import request
from ActionQueue.queue import __Queue
from ActionQueue.queue import Action
from concurrent.futures import ThreadPoolExecutor
import socket


app = Flask(__name__)

executor = ThreadPoolExecutor(1)

#NAO_IP = '192.168.1.102'
#NAO_PORT = '9559'
Q = __Queue()




@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/add_action", methods=["GET", "POST"])
def add_move():

    if "type" not in request.json:
        return "Action type not provided in request", 400
    if "command" not in request.json:
        return "Command not provided in request", 400

    if "text" not in request.json:
        action = Action(request.json['type'], request.json['command'])
    else:
        action = Action(request.json['type'], request.json['command'], request.json['text'], request.json['volume'],
                        request.json['speech_speed'])

    Q.add_to_queue(action)
    return "success", 200


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def initialize_queue():
    Q.queue_listener()


@app.before_first_request
def initialize():
    executor.submit(initialize_queue)
    return "queue listener initialized"


if __name__ == "__main__":
    app.run(threaded=True, processes=2, host="192.168.1.106", port="5000")

