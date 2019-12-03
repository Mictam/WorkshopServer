from queue import __Queue
from pepper_handler import *
import qi
import json
import datetime
#----------------------------------------------------------------------------------------------------------------------#
global Q
global NAO_IP
NAO_IP = '192.168.1.104'
global NAO_PORT
NAO_PORT = '9559'

Q = __Queue()
#---------------------------------------------------PRIVATE METHODS----------------------------------------------------#
def enqueue_speech(text, volume, speech_speed, language):
    speech_object = Speech(text, volume, speech_speed, language)
    Q.add_to_queue(speech_object)

def enqueue_moving(distance):
    print("moving  enqueued")
    movement_object = Movement(distance)
    Q.add_to_queue(movement_object)

def enqueue_turning(angle):
    turn_object = Turn(angle)
    Q.add_to_queue(turn_object)

def enqueue_sequence_execution(name):
    sequence_object = Sequence(name)
    Q.add_to_queue(sequence_object)

def enqueue_media_display(photo_or_movie_name, file_type):
    media_display_object = MediaDisplay(photo_or_movie_name, file_type)
    Q.add_to_queue(media_display_object)

#Classes Speech, Movement, Turn, Sequence, MediaDisplay all inherit from virtual Action class and all have method process_action()
#where Pepper API is called

#---------------------------------------------------PUBLIC METHODS-----------------------------------------------------#
def initialize_queue():
    Q.queue_listener()
#----------------------------------------------------------------------------------------------------------------------#
def handle_connect_request(json_request):
    print("handling connect request")       ####DEPRECIATED
    try:
        session = qi.Session()
        print(json_request)
        session.connect("tcp://{}:{}".format(json_request['IP'], json_request['port']))
        print(json_request)
    except:
        return ("Couldnt connect to the robot"), 400

    return "Successfully connected to the robot", 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_logger_request():
    print("handle_logger_request")


    session1 = qi.Session()
    session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    battery_service1 = session1.service("ALBatteryProxy")
    camera_service1 = session1.service("ALVideoRecorderProxy")
    print("xd")

    try:
        json_logger = {'is_queue_empty': Q.is_empty(), 'battery': battery_service1.getBatteryCharge() + "%",
                    'is_recording': camera_service1.isRecording()}
        response = json.dumps(json_logger)
    except:
        return ("Couldnt get logs"), 400

    return response, 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_scenarios_list_request():
    print("handle_scenarios_list_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_creating_new_scenario_request(json_request):
    print("handle_creating_new_scenario_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_deleting_scenario_request(scenario_name):
    print("handle_deleting_scenario_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_scenario_run_request(name, run, start, end):
    print("handle_scenario_run_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_modify_scenario_request(scenario_name):
    print("handle_modify_scenario_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_sequences_list_request():
    print("handle_sequences_list_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_media_list_request():
    print("handle_media_list_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_recording_toggle_request(request):
    print("handle_recording_toggle_request")
    if "status" not in request.args:
        return '"Start Date" not provided in request', 400
    camera_service = session.service("ALVideoRecorderProxy")
    if (request.args.get("status")):
        camera_service.stopRecording()
    else:
        timestamp = datetime.datetime.now().isoformat()
        camera_service.startRecording("../Videos", timestamp)

    return "Success", 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_recordings_list_request():
    print("handle_recordings_list_request")
    #todo
    json_logger1 = {'name': "VID001", 'file_type': "MP4", 'duration': 13}
    json_logger2 = {'name': "VID002", 'file_type': "MP4", 'duration': 213}
    response = json.dumps(json_logger1, json_logger2)

    return response, 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_play_recording_request(name):
    print("handle_play_recording_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_get_settings_request():
    print("handle_get_settings_request")
    #leave unimplemented
#----------------------------------------------------------------------------------------------------------------------#
def handle_set_settings_request(json_request):
    print("handle_set_settings_request")
    #leave unimplemented
#----------------------------------------------------------------------------------------------------------------------#
def handle_clear_queue_request():
    print("handle_clear_queue_request")
    try:
        Q.clear_queue()
    except:
        return 'Failed', 400
    return 'Success',  200
#----------------------------------------------------------------------------------------------------------------------#
def handle_add_action_request(json_request):
    print("handle_add_action_request")
    print(json_request)
    if "type" in json_request:
        if json_request["type"] == "speech":
            text = json_request["text"]
            volume = json_request["volume"]
            speech_speed = json_request["speech_speed"]
            language = json_request["language"]
            enqueue_speech(text, volume, speech_speed, language)

        elif json_request["type"] == "movement":
            command = json_request["command"]
            if command == "move_forward":
                distance = json_request["distance"]
                enqueue_moving(distance)
            elif command == "move_backward":
                print(float(json_request["distance"]))
                distance = float(json_request["distance"]) * (-1.0)
                enqueue_moving(distance)
            elif command == "turn_right":
                angle = float(json_request["angle"]) * (-1.0)
                enqueue_turning(angle)
            elif command == "turn_left":
                angle = json_request["angle"]
                enqueue_turning(angle)

        elif json_request["type"] == "sequence":
            name = json_request["name"]
            enqueue_sequence_execution(name)

        elif json_request["type"] == "media":
            photo_or_movie_name = json_request["name"]
            file_type = json_request["file_type"]
            enqueue_media_display(photo_or_movie_name, file_type)
        else:
            return "Wrong JSON format provided", 400

    return "Success", 200
#----------------------------------------------------------------------------------------------------------------------#

