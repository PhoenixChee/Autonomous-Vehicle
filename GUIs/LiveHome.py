monitorOn = False
controlCloseLoop = False


def switchODrive(toggle):
    global monitorOn
    if toggle.get() == 1:
        monitorOn = True
    elif toggle.get() == 0:
        monitorOn = False
        
        
def switchControlLoop(toggle):
    global controlCloseLoop
    if toggle.get() == 1:
        controlCloseLoop = True
        print('Mode: Close Loop')
    elif toggle.get() == 0:
        controlCloseLoop = False
        print('Mode: Open Loop')
        
    import shared_variables
    shared_variables.controlCloseloop = controlCloseLoop

    
print('Imported LiveDashboard.py')
