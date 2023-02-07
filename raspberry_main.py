# Import Modules
import inputs
import socket
import subprocess
import time
from threading import Timer, Thread

# Import Json
import json
with open('./config_main.json', 'r') as file:
    data = json.load(file)

# Import Raspberry Pi Packages
import board
import busio
import RPi.GPIO as gpio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Import ODrive Packages
from odrive.enums import *
from odrive.utils import *

# Import GUI Prorgam
import GUI
from GUIs.LiveButtons import keybindCommandDict

# User, IP Addresses, Port
user_rpi =  data['user']['raspberry']
eth0_ip_rpi = data['ip']['raspberry']
user_jetson = data['user']['jetson']
eth0_ip_jetson = data['ip']['jetson']
port = data['port']

terminate_socket = False

# Jetson Python File Name
jetson_main = data['fileName']['jetson']

# Steering Linear Actuator Driver Pins
pwm = 19
steering_direction = 26

# Steering Linear Actuator Limit Switch Pins
left_limit = 23
right_limit = 24

# Steering Potentiometer Address & Config
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
left_steering_encoder = AnalogIn(ads, ADS.P0)
right_steering_encoder = AnalogIn(ads, ADS.P1)

steering_tolerance = 100
digital_steer = 0


# Initialise Raspberry Pi GPIO Pins
def initialise():
    gpio.setmode(gpio.BCM)
    gpio.setup(steering_direction, gpio.OUT)
    gpio.output(steering_direction, False)
    gpio.setup(pwm, gpio.OUT)
    gpio.output(pwm, False)

    gpio.setup(left_limit, gpio.IN)
    gpio.setup(right_limit, gpio.IN)
    
    
# <<<Sockets and SSH>>> #
def start_server():
    global server_socket, conn_jetson
    
    print('Server Start')
    
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((eth0_ip_rpi, port))
    except socket.error:
        print(str(socket.error))
    
    print(f'Server is listening on port: {port}...')
    
    conj = Timer(1, connect_jetson)
    conj.start()
    
    server_socket.listen()
    conn_jetson, addr = server_socket.accept()
    print(f'Connected to: {addr[0]}:{str(addr[1])}')
    print('Connection Success')

    
def connect_jetson():
    subprocess.run(['sudo', 'ssh', f'{user_jetson}@{eth0_ip_jetson}', f'python3 /home/brushlessdc/Desktop/{jetson_main}'])
    

def jetson_client_handler(client):
    global terminate_socket
    
    while not terminate_socket: 
        data_jetson = client.recv(1024)
        
        if not data_jetson:
            break
        
        import shared_variables
        dic = json.loads(data_jetson.decode('utf-8'))
        update_dic(dic, shared_variables.odrive_dic)
        
    print(f'Terminate = {terminate_socket}')
    
    
# <<<Steering>>> #
def set_motor_power(direction):
    # Steer Right
    if direction == -1:
        gpio.output(steering_direction, True)
        gpio.output(pwm, True)
        return
    # Steer Left
    elif direction == 1:
        gpio.output(steering_direction, False)
        gpio.output(pwm, True)
        return
    # Stop
    else:
        gpio.output(steering_direction, False)
        gpio.output(pwm, False)
        return


def read_steering_encoder(steering_encoder):
    if steering_encoder == 1:
        steering_encoder_val = left_steering_encoder.value
    else:
        steering_encoder_val = right_steering_encoder.value
    
    return steering_encoder_val


def steer_to_angle(target_angle, encoder):
    current_angle = read_steering_encoder(encoder)
    
    if abs(target_angle - current_angle) < steering_tolerance:
        return
    elif target_angle > current_angle:
        while not gpio.input(left_limit) and not abs(target_angle - current_angle) < steering_tolerance:
            set_motor_power(1)
            current_angle = read_steering_encoder(encoder)
            print(f'Current_angle: {current_angle}')
        set_motor_power(0)
    elif target_angle < current_angle:
        while not gpio.input(right_limit) and not abs(target_angle - current_angle) < steering_tolerance:
            set_motor_power(-1)
            current_angle = read_steering_encoder(encoder)
            print(f'Current_angle: {current_angle}')
        set_motor_power(0)
    
    
def steering_cal():
    global left_steering_range
    global left_center_angle 
    global left_max_mean_left_encoder, right_max_mean_left_encoder
    global left_max_mean_right_encoder, right_max_mean_right_encoder

    left_max_mean_left_encoder = 0
    right_max_mean_left_encoder = 0
    
    left_max_mean_right_encoder = 0
    right_max_mean_right_encoder = 0
    
    print('Steering Calibration Initiated')

    # Steer to Max Left & Calibrate Both Potentiometer
    while not gpio.input(left_limit):
        set_motor_power(1)
        print('Left Limit: ', gpio.input(left_limit))
        time.sleep(0.01)
    print('Left Limit Hit')
    set_motor_power(0)
    
    for _ in range(10):
        reading = read_steering_encoder(1)
        left_max_mean_left_encoder += reading
    left_max_mean_left_encoder /= 10
    # for _ in range(10):
    #     reading = read_steering_encoder(0)
    #     left_max_mean_right_encoder += reading
    # left_max_mean_right_encoder /= 10
    
    # Steer to Max Right & Calibrate Both Potentiometer
    while not gpio.input(right_limit):
        set_motor_power(-1)
        print('Right Limit: ', gpio.input(right_limit))
        time.sleep(0.01)
    print('Right Limit Hit')
    set_motor_power(0)
    
    for _ in range(10):
        reading = read_steering_encoder(1)
        right_max_mean_left_encoder += reading
    right_max_mean_left_encoder /= 10
    # for _ in range(10):
    #     reading = read_steering_encoder(0)
    #     right_max_mean_right_encoder += reading
    # right_max_mean_right_encoder /= 10
    
    # Mono-Encoder Steering
    left_steering_range = abs(left_max_mean_left_encoder - right_max_mean_left_encoder)
    left_center_angle = left_steering_range / 100 * 52 + right_max_mean_left_encoder
    
    steer_to_angle(left_center_angle, 1)
    
    print('Left Encoder')
    print(f'Left Max Mean Value: {round(left_max_mean_left_encoder, 2)}')
    print(f'Right Max Mean Value {round(right_max_mean_left_encoder, 2)}')
    print(f'Steering Range: {round(left_steering_range, 2)}')
    print(f'Centre Estimate: {round(left_center_angle, 2)}')
    
    set_motor_power(0)
    print('Steering Calibration Complete')


def steering_to_center():
    global digital_steer

    conn_jetson.send(bytes('angle' + str(0), encoding = 'utf-8'))
    steer_to_angle(left_center_angle, 1)
    
    dic = {'steer_angle': 0}
    
    import shared_variables
    update_dic(dic, shared_variables.steer_dic)
    

def steering(state):
    global digital_steer
    
    if state == -1 and digital_steer > -5:
        digital_steer -= 1
    if state == 1 and digital_steer < 5:
        digital_steer += 1
        
    conn_jetson.send(bytes('angle' + str(digital_steer), encoding = 'utf-8'))
    steer_to_angle(left_steering_range / 10 * digital_steer + (left_center_angle), 1)
    
    dic = {'steer_angle': digital_steer * 3}
    
    import shared_variables
    update_dic(dic, shared_variables.steer_dic)


def update_dic(dic, shared_dic):
    shared_dic.update(dic)


def controller_command_handling():
    global digital_steer, terminate_socket, conn_jetson
    
    while True:
        events = inputs.get_gamepad()
        for event in events:
            # print(event.ev_type, event.code, event.state)
            
            # Check if Controller Bind Exist
            if (event.code in keybindCommandDict):
                # Highlight Button in GUI
                keybindCommandDict[event.code](event.state)
            
            # BUTTONS OVERVIEW #
            # CONTROL LOOP              >>> BTN_START       >>> Start
            # DISCONNECT                >>> BTN_BACK        >>> Back
            # MOTOR FORWARD/BACKWARD    >>> ABS_HAYOY       >>> △ & ▽
            # STEER LEFT/RIGHT          >>> ABS_HAY0X       >>> ◁ & ▷
            # STEER CALIBRATION         >>> BTN_NORTH       >>> Y
            # STEER TO CENTER           >>> BTN_SOUTH       >>> A
            # MOTOR STOP                >>> BTN_EAST        >>> B
            # MOTOR CALIBRATION         >>> BTN_WEST        >>> X
            # START TRAINING            >>> BTN_TR          >>> RB
            # STOP TRAINING             >>> BTN_TL          >>> LB
            # ENABLE MOTOR CONTROL      >>> ABS_Z & ABS_RZ  >>> LT & LB 
            
            # Steering Calibration
            if event.code == 'BTN_START' and event.state == 1:
                print('Control Loop')
            # Quit Program
            elif event.code == 'BTN_BACK' and event.state == 1:
                set_motor_power(0)
                gpio.cleanup()
                conn_jetson.send(b'disconnect')
                time.sleep(1)
                terminate_socket = True
                conn_jetson.shutdown(socket.SHUT_RDWR)
                conn_jetson.close()
                return
              
            # Action Buttons (X)(Y)(A)(B)
            elif event.code == 'BTN_NORTH' and event.state == 1:
                steering_cal()
            elif event.code == 'BTN_SOUTH' and event.state == 1:
                steering_to_center()
            elif event.code == 'BTN_EAST' and event.state == 1:
                conn_jetson.send(b'motor_stop')
            elif event.code == 'BTN_WEST' and event.state == 1:
                conn_jetson.send(b'motor_calibration')
            
            # Trigger Buttons
            elif event.code == 'BTN_TR' and event.state == 1:
                conn_jetson.send(b'start_training')
            elif event.code == 'BTN_TL' and event.state == 1:
                conn_jetson.send(b'stop_training')
                
            # D-Pad Buttons
            # Patching Buttons with 3 States
            elif 'ABS_HAT0Y' in event.code:
                # Drive Forward
                if (event.state == -1):
                    keybindCommandDict[event.code+'_-1'](1)
                    conn_jetson.send(b'motor_forward')
                # Drive Backwards
                elif (event.state == 1):
                    keybindCommandDict[event.code+'_1'](1)
                    conn_jetson.send(b'motor_reverse')
                # No Input
                else:
                    keybindCommandDict[event.code+'_-1'](0)
                    keybindCommandDict[event.code+'_1'](0)
                    
            # Patching Buttons with 3 States
            elif 'ABS_HAT0X' in event.code:
                # Steering Left
                if (event.state == -1):
                    keybindCommandDict[event.code+'_-1'](1)
                    steering(event.state)
                # Steering Right
                elif (event.state == 1):
                    keybindCommandDict[event.code+'_1'](1)
                    steering(event.state)
                # No Input
                else:
                    keybindCommandDict[event.code+'_-1'](0)
                    keybindCommandDict[event.code+'_1'](0)


# Start Function as Background Thread
def start_thread(name, target):
    thread = Thread(name=name, target=target, daemon=True)
    thread.start()


def main():
    start_server()
    start_thread('Jetson Client Handler', lambda:jetson_client_handler(conn_jetson))

    initialise()
    set_motor_power(0)
    time.sleep(3)
    steering_cal()

    start_thread('Controller Command Handler', lambda:controller_command_handling())
    GUI.main()


def exit():
    global terminate_socket
    
    set_motor_power(0)
    gpio.cleanup()
    conn_jetson.send(b'disconnect')
    time.sleep(1)

    terminate_socket = True
    conn_jetson.shutdown(socket.SHUT_RDWR)
    conn_jetson.close()
    
    print('Raspberry Pi Ended') 
    
    
if __name__ == '__main__':
    main()
    exit()
