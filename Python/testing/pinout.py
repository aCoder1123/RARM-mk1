"""
simple file to get json data from the json to python script
"""

import json
import os 

def getPins() -> dict:
    if str(os.getcwd())[-6:len(str(os.getcwd()))] == "Python":
        fPinouts = open(file="pinouts.json")
        pins = json.load(fPinouts)
    else:
        fPinouts = open(file="Python/pinouts.json")
        pins = json.load(fPinouts)

    fPinouts.close()
    return pins

print(getPins())

