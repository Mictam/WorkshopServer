from flask import Flask
from flask import jsonify, request, redirect, Response, render_template
from Queue.queue import __Queue
from concurrent.futures import ThreadPoolExecutor
from Settings.robot_settings import Settings
from Video_manager.video_manager import *

app = Flask(__name__)

executor = ThreadPoolExecutor(1)



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
    return "success", 200

@app.route("/connect", methods=["GET"])
def connect():
    if "ip" not in request.args:
        return "Robot IP not provided in request", 400
    ip = request.args.get('ip')

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

