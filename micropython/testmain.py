from machine import Pin
import json
import time

while True:
    an = Pin(5, Pin.IN)
    bereit = Pin(4, Pin.IN)
    fehler = Pin(14, Pin.IN)

    if an.value() == 1:
        print("An")
    if bereit.value() == 1:
        print("Bereit")
    if fehler.value() == 1: 
        print("Fehler")