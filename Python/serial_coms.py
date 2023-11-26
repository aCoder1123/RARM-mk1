import serial
import time

# port = '/dev/ttyACM0'
# print(port)
# ser = serial.Serial(port, 9600, timeout=1)

# while True:
#     # ser.write(b"Hello from Raspberry Pi!\n")
#     line = ser.readline().decode('utf-8').rstrip()
#     print(line)
#     time.sleep(1)
    
def set_serial():
    print("testing")
    
    port = '/dev/ttyACM0'
    print(port)
    serial_connection = serial.Serial(port, 9600, timeout=1)
    serial_connection.reset_input_buffer()
    return serial_connection

def read_pin(pin, ser: serial.Serial):
    ser.write(str(pin).encode('utf-8'))
    
    i=0
    while i < 10000:
        i+=1
        number = ser.read_until('\n')
        if number != b'':
            reading = int(number.decode('utf-8'))
            ser.reset_input_buffer()
            return reading
    
    return -1

# while True:
#     serial_conn = set_serial()
#     print(read_pin(1, serial_conn))
#     time.sleep(1)