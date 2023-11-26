from serial_coms import set_serial, read_pin

serial_conn = set_serial()

for i in range(100):
    pin = input("Enter Pin: ")
    print(read_pin(pin, serial_conn))
    