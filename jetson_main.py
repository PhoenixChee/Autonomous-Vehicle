# Import Modules
import os
import socket
import subprocess
import time
from threading import Timer, Thread

# Import Json
import json
with open('/home/brushlessdc/Desktop/config_main.json', 'r') as file:
    data = json.load(file)

# Import OpenCV
import cv2
import csv

# Import ODrive Modules
from odrive.enums import *
from odrive.utils import *

# User, IP Addresses, Port
user_rpi = data['user']['raspberry']
eth0_ip_rpi = data['ip']['raspberry']
user_jetson = data['user']['jetson']
eth0_ip_jetson = data['user']['jetson']
port = data['port']

training_started = False
terminate = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((eth0_ip_rpi, port))

cam = cv2.VideoCapture(0)

jetson_mode = 'NIL'
digital_steer = 0


command_instruction = {
    'motor_calibration':lambda:calibration_m1(),
    'motor_forward':lambda:move_m1(data['motorSettings']['forwardSpeed']),
    'motor_reverse':lambda:move_m1(data['motorSettings']['reverseSpeed']),
    'motor_stop':lambda:move_m1(0),
    'start_training':lambda:start_training(),
    'stop_training':lambda:stop_training(),
    'disconnect':lambda:disconnect()
}


# ODrive Axis States List in Strings 
axis_states = [
    'Undefined', 
    'Idle', 
    'Startup Sequence', 
    'Motor Calibration', 
    'Encoder Index', 
    '', 
    'Encoder Index Search', 
    'Encoder Offset Calibration', 
    'Closed Loop Control', 
    'Lockin Spin',
    'Encoder Dir Find', 
    'Homing', 
    'Encoder Hall Polarity Calibration', 
    'Encoder Hall Phase Calibration'
]


def send_dic():
    global odrv, server, terminate
    
    while not terminate:
        try:
            odrive_dic = {
                'battery_voltage': odrv.vbus_voltage,
                'control_mode': odrv.axis1.controller.config.control_mode,
                'm0_state': get_state_result(odrv.axis0.current_state),
                'm1_state': get_state_result(odrv.axis1.current_state),
                'm0_velocity': odrv.axis0.encoder.vel_estimate,
                'm1_velocity': odrv.axis1.encoder.vel_estimate,
                'm0_current': odrv.axis0.motor.current_control.Iq_measured,
                'm1_current': odrv.axis1.motor.current_control.Iq_measured,
                'm0_calibration': get_error_boolean(odrv.axis0.motor.is_calibrated),
                'm1_calibration': get_error_boolean(odrv.axis1.motor.is_calibrated),
                'watchdog_timer': get_error_boolean(odrv.axis1.config.enable_watchdog),
                'a1_system_error': get_error_boolean(odrv.error),
                'a1_motor_error': get_error_boolean(odrv.axis1.motor.error),
                'a1_controller_error': get_error_boolean(odrv.axis1.controller.error),
                'a1_encoder_error': get_error_boolean(odrv.axis1.encoder.error)
            }
        except:
            print('tough')
            odrv = odrive.find_any()
            print(f'ODrive Retrieve: {odrv}')
        
        server.send(bytes(str(json.dumps(odrive_dic)), encoding = 'utf-8'))
        time.sleep(data['odriveSettings']['pollingRate'])


def get_error_boolean(data):
    if data == 0 or 'False':
        result = 'No Error'
    elif data == 1 or 'True':
        result = 'Error'
    else:
        result = 'Unknown'
    return result


def get_state_result(data):
    result = axis_states[data]
    return result
        
    
# <<<ODRIVE>>> #
def power():
    global odrv, odrv_status
    
    odrv = odrive.find_any()
    print(f'ODrive Retrieve: {odrv}')
    
    odrv.clear_errors()

    
def calibration_m1():
    global odrv
    
    try:
        odrv.clear_errors()
        odrv.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        time.sleep(10)
        odrv.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        dump_errors(odrv)
    except:
        print('Error in Calibration')
        
        odrv = odrive.find_any()
        print(f'ODrive Retrieve: {odrv}')


def move_m1(speed):
    odrv.axis1.controller.input_vel = speed


def command_handling():
    global terminate, digital_steer
    
    while not terminate:
        data = server.recv(1024)
        
        if not data:
            break
        
        command = str(data.decode('ascii'))
        print(command)
        
        if command[:5] == 'angle':
            digital_steer = int(command[5:7])
            print(command[5:7])
        elif command not in command_instruction: 
            continue
        else:
            command_instruction[command]()
    
    print('Command Handling Terminated')


def gather_training_data():
    global terminate_training, digital_steer, img_counter, cam
    
    print('Training Initialise')
    #CV2
    img_counter = 0
    video = 'video'
    dtbase = ['folder']
    capture = ['center', 'steering']
    capture_delay = 20		#capturing delay for traing data in ms
    
    #pathing and folder creation for new training data 
    with open('/home/brushlessdc/Desktop/dtbase.csv', 'r') as file:
        folderid= int(file.read())
    path = '/home/brushlessdc/Documents/IMG' + str(folderid)
    os.umask(0)
    os.mkdir(path, mode=0o777)  # mode =0o777 gives permission to read write and execute to everyone (may be a security vunerability)
    newpath = os.path.join(path, 'capture.csv')
    
    print('Training Initialise Success')
    
    while not terminate_training:
        print('Training In Progress')
        result, image = cam.read()
        Cat = ['center', 'steering']
    
        print(cam.isOpened())
        if result:
            #cv2.imshow(video, image)
            cv2.waitKey(capture_delay)
            img_name = f'center_{img_counter}.png'
            file = os.path.join(path, img_name)
            cv2.imwrite(file, image)
            img_counter += 1
            angle = digital_steer
            dict = {'center': file, 'steering': angle}
            
            with open(newpath, 'a') as csv_file:
                dict_object = csv.DictWriter(csv_file, fieldnames = Cat) 
                dict_object.writerow(dict)
            

    print('Training Exited')
    #cv2.destroyWindow(video)
    folderid += 1
    dict = {'folder': folderid}
    with open('/home/brushlessdc/Desktop/dtbase.csv', 'w') as file:
        dict_object = csv.DictWriter(file, fieldnames = dtbase) 
        dict_object.writerow(dict)
        
    return


def start_training():
    global terminate_training, training_started, jetson_mode
    
    terminate_training = False
    jetson_mode = 'training'

    
    
def stop_training():
    global terminate_training, training_started, jetson_mode
    
    jetson_mode = 'NIL'
    training_started = False
    terminate_training = True
 
 
def disconnect():
    global odrv, terminate, terminate_training, cam
    
    odrv.axis1.requested_state = AXIS_STATE_IDLE
    #server.shutdown(socket.SHUT_RDWR)
    cam.release()
    server.close()
    del odrv
    
    terminate_training = True
    terminate = True
    
    print(f'terminate = {terminate}')


def startThread(name, target):
    thread = Thread(name=name, target=target, daemon=True)
    thread.start()


def Jetson_AI():
    global jetson_mode, terminate
    
    while not terminate:
        if jetson_mode == 'training':
            gather_training_data()
        elif jetson_mode == 'auto':
            print('Auto Mode')
    
    time.sleep(2)
    print('Jetson AI Ended')


if __name__ == '__main__':
    power()
    startThread('command handling', lambda:command_handling())
    startThread('send dic', lambda:send_dic())
    Jetson_AI()
