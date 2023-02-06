from GUI import data
from PIL import Image, ImageTk

import cv2

camOn = False
currentCamSettings = {}
currentImageSettings = {}


# switchCamera() sets up and configures the camera
def switchCamera(frame, toggle):
    global camOn, cap

    # Camera Port
    cap = cv2.VideoCapture(data['camSettings']['port'])

    # Configure Camera Settings
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, data['camSettings']['resolutionWidth'])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, data['camSettings']['resolutionHeight'])
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FPS, data['camSettings']['targetFPS'])

    if toggle.get() == 1:
        camOn = True
        showFrames(frame)
    elif toggle.get() == 0:
        camOn = False
        cap.release()
        showCameraDisabled(frame)


# showFrames() reads the captured frames and display them as a image using Pillow
def showFrames(frame):
    if camOn:
        # Capture Video Frames & Convert to OpenCV (BGR) to PIL (RGB) Color Convention Format
        cv2Frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        cv2Frame = cv2.resize(cv2Frame, (data['imageSettings']['width'], data['imageSettings']['height']))
        img = Image.fromarray(cv2Frame)

        # Configure Target Frame as PIL Image
        imgtk = ImageTk.PhotoImage(image=img)
        frame.imgtk = imgtk
        frame.configure(image=imgtk)
        frame.after(int(1000/data['imageSettings']['targetFPS']), lambda: showFrames(frame))


# showCemeraDisbled() show camera-disabled.png
def showCameraDisabled(frame):
    photo = ImageTk.PhotoImage(file='./GUIs/Images/camera-disabled.png')
    frame.photo = photo # Hold a reference to the TkInter object by attaching it to a widget(frame) attribute 
    frame.configure(image=photo)


# camSettings() gets the actual camera configurations
def camSettings():
    currentCamSettings['widthResolution'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    currentCamSettings['heightResolution'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    currentCamSettings['targetFPS'] = int(cap.get(cv2.CAP_PROP_FPS))
    
    return currentCamSettings


# imageSettings() gets the actual image configurations
def imageSettings():
    currentImageSettings['imageWidth'] = data['imageSettings']['width']
    currentImageSettings['imageHeight'] = data['imageSettings']['height']
    currentImageSettings['imageFPS'] = data['imageSettings']['targetFPS']

    return currentImageSettings


print('Imported LiveCam.py')
