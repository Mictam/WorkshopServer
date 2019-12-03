from flask import Flask
from flask import request
from ActionQueue.queue import __Queue
from ActionQueue.queue import Action
from concurrent.futures import ThreadPoolExecutor
import socket
import werkzeug
import qi
import json
import datetime


app = Flask(__name__)

executor = ThreadPoolExecutor(1)

#NAO_IP = '192.168.1.102'
#NAO_PORT = '9559'
Q = __Queue()




@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/connect', methods=["GET"])
def connect():


    result = handle_connect(request.json)



    try:
        session = qi.Session()
        session.connect("tcp://{}:{}".format("192.168.1.102", 9559))
    except:
        return("Couldnt connect to the robot"), 400

    return "Successfully connected to the robot", 200

@app.route('/logger', methods=["GET", "POST"])
def logger():
    try:
        session = qi.Session()
        session.connect("tcp://{}:{}".format("192.168.1.102", 9559))
        battery_service = session.service("ALBatteryProxy")
        camera_service = session.service("ALVideoRecorderProxy")
        json_logger = {'is_queue_empty': Q.is_empty(), 'battery': battery_service.getBatteryCharge() + "%", 'is_recording': camera_service.isRecording()}
        response = json.dumps(json_logger)
    except:
        return("Couldnt get logs"), 400

    return response, 200


@app.route('/settings', methods=["GET", "POST"])
def logger():
    try:
        session = qi.Session()
        session.connect("tcp://{}:{}".format("192.168.1.102", 9559))
        speech_service = session.service("ALTextToSpeechProxy")
        if request.method == 'GET':
            json_logger = {'volume': speech_service.getVolume(), 'speech_speed': speech_service.getParameter("speed")}
            response = json.dumps(json_logger)
        else:
            speech_service.setVolume(request.json['volume'])
            speech_service.setParameter("speed", request.json['speech_speed'])
            response = "Success"
    except:
        return("Couldnt get/set setting info"), 400

    return response, 200


@app.route('/sequences', methods=["GET"])
def get_sequences():
    #TODO
    json_logger1 = {'name': "wave right arm"}
    json_logger2 = {'name': "cha cha dance"}
    response = json.dumps(json_logger1, json_logger2)

    return response, 200


@app.route('/media', methods=["GET"])
def get_media():
    #TODO
    json_logger1 = {'name': "IMG001", 'file_type': "JPG"}
    json_logger2 = {'name': "VID002", 'file_type': "MP4", 'duration': 213}
    response = json.dumps(json_logger1, json_logger2)

    return response, 200

@app.route('/record', methods=["GET"])
def record():
    if "status" not in request.args:
        return '"Start Date" not provided in request', 400
    session = qi.Session()
    session.connect("tcp://{}:{}".format("192.168.1.102", 9559))
    camera_service = session.service("ALVideoRecorderProxy")
    if(request.args.get("status")):
        camera_service.stopRecording()
    else:
        timestamp = datetime.datetime.now().isoformat()
        camera_service.startRecording("../Videos", timestamp)

    return "Success", 200

@app.route('/recordings', methods=["GET"])
def get_recordings():
    #TODO
    json_logger1 = {'name': "VID001", 'file_type': "MP4", 'duration': 13}
    json_logger2 = {'name': "VID002", 'file_type': "MP4", 'duration': 213}
    response = json.dumps(json_logger1, json_logger2)

    return response, 200


@app.route('/upload_photo', methods = ['GET', 'POST'])
def handle_request():
    imagefile = request.files['image']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    imagefile.save(filename)
    return "Image Uploaded Successfully", 200


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
                        request.json['speech_speed'], request.json['language'])

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

@app.route('/clear_queue')
def clear_queue():
    Q.clear_queue()
    return "success", 200




@app.before_first_request
def initialize():
    executor.submit(initialize_queue)
    return "queue listener initialized"


if __name__ == "__main__":
    app.run(threaded=True, processes=2, host="192.168.1.106", port="5000")

