import numpy as np

steerAngleMin = -15.0
steerAngleMax = 15.0

speedMin = -0.3 * 60
speedMax = 0.3 * 60

steerAngleDict = {}
speedDict = {}


def readSteerAngle():
    import shared_variables
    
    dict = steerAngleDict
    dict['currentSteerAngle'] = shared_variables.steering_angle
    dict['percentageSteerAngle'] = 50 + round(convert2Percentage(steerAngleMin, steerAngleMax, dict['currentSteerAngle']), 2)
    
    return dict
    
    
def readSpeed():
    import shared_variables
    
    dict = speedDict
    dict['currentSpeed'] = round(shared_variables.m1_speed * 60, 2)
    dict['percentageSpeed'] = 50 + round(convert2Percentage(speedMin, speedMax, dict['currentSpeed']), 2)
    
    return dict


def convert2Percentage(min, max, input):
    percentageValue = (input/(max-min))*100
    return percentageValue
