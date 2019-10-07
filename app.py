from flask import Flask
from flask import jsonify, request, redirect, Response, render_template
from Queue.queue import __Queue
from Queue.queue import Action
from concurrent.futures import ThreadPoolExecutor
from Settings.robot_settings import Settings
from Video_manager.video_manager import *

import qi
import sys

app = Flask(__name__)

executor = ThreadPoolExecutor(1)

NAO_IP = '192.168.1.102'
NAO_PORT = 9559



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/add_action", methods=["GET", "POST"])
def add_move(Q = __Queue):

    if "type" not in request.json:
        return "Action type not provided in request", 400
    if "command" not in request.json:
        return "Command not provided in request", 400

    if "text" not in request.json:
        action = Action(request.json['type'], request.json['command'])
    else:
        action = Action(request.json['type'], request.json['command'], request.json['text'])

    __Queue.add_to_queue(Q, action)

    return "success", 200

@app.route("/connect", methods=["GET", "POST"])
def connect():
    if "ip" not in request.args:
        return "Robot IP not provided in request", 400
    if "port" not in request.args:
        return "Robot port not provided in request", 400
    ip = request.args.get('ip')
    port = request.args.get('port')

    NAO_IP = ip
    NAO_PORT = port

    session = qi.Session()

    try:
        session.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + NAO_IP + "\" on port " + str(NAO_PORT) + ".\n"
                                                                                           "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    return "success", 200


@app.route("/settings",  methods=["POST"])
def set_robot():
    if not request.json:
        return "Robot Settings not provided", 400
    try:
        settings = Settings.change_settings(request.json['robot_language'],
                             request.json['voice'],
                             request.json['volume'],
                             request.json['app_language']
                             )
        settings.send_settings_to_robot()
        return "success", 200
    except KeyError as e:
        return "Value of {} missing in given JSON".format(e), 400


@app.route('/video/delete', methods=["GET"])
def delete_video():
    if "id" not in request.args:
        return "Video ID not provided in request", 400
    id = request.args.get('id')
    remove_video(id)
    return "success", 200


@app.route('/video/info', methods=["GET"])
def info_video():
    if "id" not in request.args:
        return "Video ID not provided in request", 400
    id = request.args.get('id')
    request_video_info(id)
    return "success", 200


@app.route('/video/play', methods=["GET"])
def play_video():
    if "id" not in request.args:
        return "Video ID not provided in request", 400
    id = request.args.get('id')
    play_video(id)
    return "success", 200


def initialize_queue(Q = __Queue):
    Q.queue_listener(Q)


@app.before_first_request
def initialize():
    executor.submit(initialize_queue)
    return "queue listener initialized"


if __name__ == "__main__":
    app.run(threaded=True,processes=2)

