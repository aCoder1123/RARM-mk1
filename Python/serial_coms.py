#!/usr/bin/env python3
import serial
import time
import os

# while True:
#     ser.write(b"Hello from Raspberry Pi!\n")
#     line = ser.readline().decode('utf-8').rstrip()
#     print(line)
#     time.sleep(1)
#     

def set_serial():
    print(os.listdir("/dev/"))
    serial_connection = serial.Serial('/dev/ttyAMC0', 9600, timeout=1)
    serial_connection.reset_input_buffer()
    return serial_connection
    
def read_pin(pin, ser):
    ser.write(str(pin).encode('utf-8'))
    
    i=0
    while i < 10000:
        i+=1
        number = ser.read()
        if number != b'':
            reading = int.from_bytes(number, byteorder='big')
            return reading
    
    return -1

# while True:
#     serial_conn = set_serial()
#     print(read_pin(1, serial_conn))
#     time.sleep(1)