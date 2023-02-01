import numpy as np

currentTempList = {}

def readTemp():
    for n in range(6):
        currentTempList[f'sensor{n}'] = round(np.random.uniform(35.0, 40.0), 2)

    return currentTempList
