from GUI import data
from GenerateData.ODrive import *
from GenerateData.Steering import *
from GUIs.LiveCam import camSettings, imageSettings
from GUIs.LiveGraph import monitorTemp

liveLabelsDict = {}     # Each Registered Label, LabelName[0] and Text[1] Dict
liveBarsDict = {}       # Each Registered Bar, BarName[0] and Value[1] Dict 
dataDict = {}           # Each Received Data Dict

updateOnce = {'home': True, 'control': True, 'cam': True, 'temp': True}


def registerLiveLabel(dataName, label, text):
    liveLabelsDict.update({dataName: [label, text]})


def registerLiveBar(dataName, bar, value):
    liveBarsDict.update({dataName: [bar, value]})


def updateLiveLabel(frame):
    # All Data Comes Through Here
    updateHomeData()
    updateControlData()
    updateCamData()
    updateTempData()

    # Get Data and Matching Labels for Update
    for keyName in dataDict:
        # Configure Label Text
        if keyName in liveLabelsDict:
            label = liveLabelsDict.get(keyName)[0]
            value = dataDict.get(keyName)
            if value == 'ERROR':
                label.config(text=value, foreground='#b4a0ff')
            else:
                label.config(text=value, foreground='')
        
        # Configure Bar Value
        if keyName in liveBarsDict:
            bar = liveBarsDict.get(keyName)[0]
            value = dataDict.get(keyName)
            bar.config(value=value)
            
    frame.after(data['labelSettings']['refreshRate'], lambda: updateLiveLabel(frame))


def getDataLabel(dict, dataList):
    for keyName in dataList:
        if keyName in dict:
            dataDict.update({f'{keyName}': str(dict.get(f'{keyName}'))})


def getDefaultLabel(key, dataList):
    updateOnce[f'{key}'] = True
    
    for keyName in dataList:
        if keyName in liveLabelsDict:
            dataDict.update({f'{keyName}': liveLabelsDict.get(keyName)[1]})
        if keyName in liveBarsDict:
            dataDict.update({f'{keyName}': liveBarsDict.get(keyName)[1]})


def updateHomeData():
    from GUIs.LiveHome import monitorOn
    from shared_variables import odrive_dic
    
    key = 'home'
    dataList = ['MF0Temp', 'MF0TempBar', 'MF1Temp', 'MF1TempBar', 'MFBrakesTemp', 'MFBrakesTempBar', 'batteryVoltage', 'batteryTemp', 'batteryTempBar', 'M0State', 'M1State', 'M0Current', 'M1Current', 'M0Velocity', 'M1Velocity', 'M0Temp', 'M1Temp', 'M0TempBar', 'M1TempBar', 'A0AxisError', 'A1AxisError', 'A0MotorError', 'A1MotorError', 'A0ControllerError', 'A1ControllerError', 'A0EncoderError', 'A1EncoderError', 'raspberryStatus', 'jetsonStatus', 'odriveStatus', 'arduinoStatus']

    # Update ODrive Data
    if monitorOn:
        updateOnce[key] = False
        getDataLabel(odriveTemperatureData() ,dataList)
        getDataLabel(motorData() ,dataList)
        getDataLabel(batteryData() ,dataList)
        getDataLabel(dashboardData() ,dataList)
        
    elif not updateOnce[key]:
        getDefaultLabel(key, dataList)
        

def updateControlData():
    from GUIs.LiveHome import controlCloseLoop
    
    key = 'control'
    dataList = ['speed', 'speedBar', 'steerAngle', 'steerAngleBar']
    
    # Update Speed Data & Steering Data
    if controlCloseLoop:
        updateOnce[key] = False
        
        # currentSpeed = readSpeed()
        # dataDict.update({'speed': str(currentSpeed.get('currentSpeed')) + ' RPM'})
        # dataDict.update({'speedBar': currentSpeed.get('percentageSpeed')})
        
        # currentAngle = readSteerAngle()
        # dataDict.update({'steerAngle': str(currentAngle.get('currentSteerAngle')) + ' °'})
        # dataDict.update({'steerAngleBar': currentAngle.get('percentageSteerAngle')})
        
        getDataLabel(speedData() ,dataList)
        getDataLabel(steerData() ,dataList)
        
    elif not updateOnce[key]:
        getDefaultLabel(key, dataList)
        

def updateCamData():
    from GUIs.LiveCam import camOn
    
    key = 'cam'
    dataList = ['camResolution', 'camFPS', 'imageResolution', 'imageFPS']
    
    # Update Camera Settings & Image Settings Data
    if camOn:
        updateOnce[key] = False

        currentCamSettings = camSettings()
        dataDict.update({'camResolution': str(currentCamSettings.get('widthResolution')) + '×' + str(currentCamSettings.get('heightResolution'))})
        dataDict.update({'camFPS': str(currentCamSettings.get('targetFPS')) + ' FPS'})
        
        currentImageSettings = imageSettings()
        dataDict.update({'imageResolution': str(currentImageSettings.get('imageWidth')) + '×' + str(currentImageSettings.get('imageHeight'))})
        dataDict.update({'imageFPS': str(currentImageSettings.get('imageFPS')) + ' FPS'})
        
    elif not updateOnce[key]:
        getDefaultLabel(key, dataList)


def updateTempData():
    from GUIs.LiveGraph import monitorOn
    
    key = 'temp'
    dataList = ['currentTemp', 'highestTemp', 'lowestTemp']

    # Update All Temperature Data
    if monitorOn:
        updateOnce[key] = False
        
        dict = monitorTemp()
        dataDict.update({'currentTemp': str(dict.get('current')) + ' °C'})
        dataDict.update({'highestTemp': str(dict.get('highest')) + ' °C'})
        dataDict.update({'lowestTemp': str(dict.get('lowest')) + ' °C'})
        
    elif not updateOnce[key]:
        getDefaultLabel(key, dataList)


# Get Data From Shared Variables

minTemp, maxTemp = 0, 100
minSpeed, maxSpeed = -0.3 * 60, 0.3 * 60

def odriveTemperatureData():
    import shared_variables
    
    sensor0 = round(shared_variables.temperature_dic['sensor_0'], 2)
    sensor1 = round(shared_variables.temperature_dic['sensor_1'], 2)
    sensor2 = round(shared_variables.temperature_dic['sensor_2'], 2)
    
    dict = {
        'MF0Temp': str(sensor0) + ' °C',
        'MF0TempBar': convert2Percentage(minTemp, maxTemp, sensor0),
        'MF1Temp': str(sensor1) + ' °C',
        'MF1TempBar': convert2Percentage(minTemp, maxTemp, sensor1),
        'MFBrakesTemp': str(sensor2) + ' °C',
        'MFBrakesTempBar': convert2Percentage(minTemp, maxTemp, sensor2),
    }
    return dict


def motorData():
    import shared_variables
    
    M0State = shared_variables.odrive_dic['m0_state']
    M1State = shared_variables.odrive_dic['m1_state']
    M0Current = round(shared_variables.odrive_dic['m0_current'], 2)
    M1Current = round(shared_variables.odrive_dic['m1_current'], 2)
    M0Velocity = round(shared_variables.odrive_dic['m0_velocity'], 2)
    M1Velocity = round(shared_variables.odrive_dic['m1_velocity'], 2)
    M0Temp = round(shared_variables.temperature_dic['sensor_0'], 2)
    M1Temp = round(shared_variables.temperature_dic['sensor_0'], 2)
    
    dict = {
        'M0State': str(M0State),
        'M1State':  str(M1State),
        'M0Current':  str(M0Current) + ' A',
        'M1Current':  str(M1Current) + ' A',
        'M0Velocity':  str(M0Velocity),
        'M1Velocity':  str(M1Velocity),
        'M0Temp': str(M0Temp) + ' °C',
        'M1Temp': str(M1Temp) + ' °C',
        'M0TempBar': convert2Percentage(minTemp, maxTemp, M0Temp),
        'M1TempBar': convert2Percentage(minTemp, maxTemp, M1Temp)
    }
    return dict


def batteryData():
    import shared_variables
    
    batteryVoltage = round(shared_variables.odrive_dic['battery_voltage'], 2)
    batteryTemp = round(shared_variables.temperature_dic['sensor_0'], 2)
    
    dict = {
        'batteryVoltage': str(batteryVoltage) + ' V',
        'batteryTemp': convert2Percentage(minTemp, maxTemp, batteryTemp)
    }
    return dict


def dashboardData():
    import shared_variables
    
    odriveStatus = shared_variables.odrive_dic['watchdog_timer']
    
    A0AxisError = shared_variables.odrive_dic['a0_system_error']
    A1AxisError = shared_variables.odrive_dic['a1_system_error']
    A0MotorError = shared_variables.odrive_dic['a0_motor_error']
    A1MotorError = shared_variables.odrive_dic['a1_motor_error']
    A0ControllerError = shared_variables.odrive_dic['a0_controller_error']
    A1ControllerError = shared_variables.odrive_dic['a1_controller_error']
    A0EncoderError = shared_variables.odrive_dic['a0_encoder_error']
    A1EncoderError = shared_variables.odrive_dic['a1_encoder_error']
    
    dict = {
        'odriveStatus': str(odriveStatus),
        'A0AxisError': str(A0AxisError),
        'A1AxisError': str(A1AxisError),
        'A0MotorError': str(A0MotorError),
        'A1MotorError': str(A1MotorError),
        'A0ControllerError': str(A0ControllerError),
        'A1ControllerError': str(A1ControllerError),
        'A0EncoderError': str(A0EncoderError),
        'A1EncoderError': str(A1EncoderError)
    }
    return dict


def speedData():
    import shared_variables
    
    M0Velocity = shared_variables.odrive_dic['m0_velocity']
    M1Velocity = shared_variables.odrive_dic['m1_velocity']
    averageSpeed = ((M0Velocity + M1Velocity)/2) * 60
    
    dict = {
        'speed': str(averageSpeed) + ' RPM',
        'speedBar': 50 + convert2Percentage(minSpeed, maxSpeed, averageSpeed)
    }
    return dict


def steerData():
    import shared_variables
    
    steerAngle = shared_variables.steer_dic['steer_angle']
    
    dict = {
        'steerAngle': str(steerAngle) + ' °',
        'steerAngleBar': 50 + convert2Percentage(-15, 15, steerAngle)
    }
    return dict


def convert2Percentage(min, max, input):
    percentageValue = (input/(max - min)) * 100
    percentageValue = round(percentageValue, 2)
    return percentageValue


print('Imported LiveLabels.py')
