from serial import Serial

baud = 115200
timeout = 0.1

ping = b'\xc0\x25\x00\x00\x00\x00\xc0'

def get_serialdevice(port: str):
    return Serial(port = port, baudrate = baud, timeout = timeout)
