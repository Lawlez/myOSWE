import serial

# establish connection to serial port
ser = serial.Serial('/dev/tty.usbserial-AB0MD2JV', 9600, timeout=1)

# send a VISCA command to the camera
def send_command(cmd):
    print(cmd)
    ser.write(cmd)
    response = ser.read(128) # read up to 128 bytes of response
    print(response)
    return response

# check connection to camera
def check_connection():
    # send the ping command
    address_set = b'\x80\x30\x01\xff'
    reset = b'\x81\x01\x04\x00\x02\xFF'
    ping_cmd = bytes.fromhex('80 01 42 ff')
    response1 = send_command(reset)
    print(response1)
    response = send_command(ping_cmd)

    # check the response
    if response == bytes.fromhex('90 50 0D 00 01 FF'):
        print('Connection to camera successful.')
        return True
    else:
        print('Connection to camera failed.')
        return False

# example commands
zoom_in = bytes.fromhex('81 01 04 07 02 FF')
zoom_out = bytes.fromhex('88 01 04 07 03 FF')

# check the connection to the camera
if check_connection():
    # send some commands to the camera
    send_command(zoom_in)
    send_command(zoom_out)

# close the serial port
ser.close()
