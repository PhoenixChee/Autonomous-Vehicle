import numpy as np

currentODriveDict = {}

oDriveInfolist = ['voltage', 'temp', 'controlLoop', 'system']
motorInfoList = ['state', 'current', 'velocity', 'temperature']
axisInfoList = ['axisError', 'motorError', 'controllerError', 'encoderError']
microcontrollerList = ['raspberry', 'jetson', 'odrive', 'arduino']

M0TempMin, M1TempMin = 30.0, 30.0
M0TempMax, M1TempMax = 35.0, 35.0
statusInfo = ['NO ERROR', 'ERROR', '-']
controllerInfo = ['CONNECTED', '-']


def readODrive():
    import shared_variables
    dict = currentODriveDict
    
    ID = 'OD'
    dict[f'{oDriveInfolist[0]}{ID}'] = round(shared_variables.battery_voltage, 2)
    dict[f'{oDriveInfolist[1]}{ID}'] = round(np.random.uniform(M1TempMin, M1TempMax), 2)
    dict[f'{oDriveInfolist[2]}{ID}'] = shared_variables.control_mode
    dict[f'{oDriveInfolist[3]}{ID}'] = 'CONNECTED'

    ID = 'M0'
    dict[f'{motorInfoList[0]}{ID}'] = shared_variables.m0_state
    dict[f'{motorInfoList[1]}{ID}'] = round(shared_variables.m0_current, 2)
    dict[f'{motorInfoList[2]}{ID}'] = round(shared_variables.m0_speed, 2)
    dict[f'{motorInfoList[3]}{ID}'] = round(np.random.uniform(M1TempMin, M1TempMax), 2)
    ID = 'M1'
    dict[f'{motorInfoList[0]}{ID}'] = shared_variables.m1_state
    dict[f'{motorInfoList[1]}{ID}'] = round(shared_variables.m1_current, 2)
    dict[f'{motorInfoList[2]}{ID}'] = round(shared_variables.m1_speed, 2)
    dict[f'{motorInfoList[3]}{ID}'] = round(np.random.uniform(M1TempMin, M1TempMax), 2)
    
    ID = 'A0'
    dict[f'{axisInfoList[0]}{ID}'] = '-'
    dict[f'{axisInfoList[1]}{ID}'] = '-'
    dict[f'{axisInfoList[2]}{ID}'] = '-'
    dict[f'{axisInfoList[3]}{ID}'] = '-'
    
    ID = 'A1'
    dict[f'{axisInfoList[0]}{ID}'] = convert2Logic(shared_variables.a1_system_error)
    dict[f'{axisInfoList[1]}{ID}'] = convert2Logic(shared_variables.a1_motor_error)
    dict[f'{axisInfoList[2]}{ID}'] = convert2Logic(shared_variables.a1_controller_error)
    dict[f'{axisInfoList[3]}{ID}'] = convert2Logic(shared_variables.a1_encoder_error)
    
    ID = 'Status'
    dict[f'{microcontrollerList[0]}{ID}'] = 'CONNECTED'
    dict[f'{microcontrollerList[1]}{ID}'] = 'CONNECTED'
    dict[f'{microcontrollerList[2]}{ID}'] = 'CONNECTED'
    dict[f'{microcontrollerList[3]}{ID}'] = '-'
    
    return dict


def convert2Percentage(min, max, input):
    percentageValue = (input/(max-min))*100
    return percentageValue


def convert2Logic(input):
    if input == 0:
        return 'NO ERROR'
    if input == 1:
        return 'ERROR'
