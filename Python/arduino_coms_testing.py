import serial_coms

serial_conn = serial_coms.set_serial()


for i in range(100):
    pin = input("Enter Pin: ")
    print(serial_coms.read_pin(pin, serial_conn))
    