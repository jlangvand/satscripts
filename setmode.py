#!/bin/python

# satscripts Copyright (C) 2021 Joakim Skogø Langvand @jlangvand

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import getopt
from serial import Serial
from socket import socket, AF_INET, SOCK_STREAM

from setup import get_serialdevice

VERSION = "setmode.py v0.3"

TCP_PORT: int = 2022
TCP_ADDR: str = "127.0.0.1"
BUFFER_SIZE: int = 1024

FEND = b'\xc0'
FESC = b'\xdb'
TFEND = b'\xdc'
TFESC = b'\xdd'

SET_MODE = b'\x29'
SET_POWER = b'\x22'


def int8(i: int) -> bytes:
    """
    Takes a signed integer and returns the 8-bit representation of it.

    :param i: Signed integer
    :return: Single byte representation
    """
    return int.to_bytes(i, length=1, byteorder="little", signed=True)


def bytes_to_str(bytes_in: bytes) -> str:
    """
    Returns a human readable hex representation of a byte array.

    :param bytes_in: Bytes to convert
    :return: Human readable hex representation
    """
    str_out = ""
    for byte in bytes_in:
        str_out += hex(byte) + " "
    return str_out


def escape_special_codes(raw_codes):
    """
    Escape special codes, per KISS spec.

    "If the FEND or FESC codes appear in the data to be transferred, they
    need to be escaped. The FEND code is then sent as FESC, TFEND and the
    FESC is then sent as FESC, TFESC."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description

    :return: Data with escaped special codes (bytestring)
    """
    out = bytearray()
    for b in raw_codes:
        if b == FEND:
            out.append(FESC)
            out.append(TFEND)
        elif b == FESC:
            out.append(b)
            out.append(TFESC)
        else:
            out.append(b)
    return out


def help():
    print("")
    print(VERSION)
    print("Script for testing/debugging Nanoavionics Sat2RF1 satellite radio")
    print("")
    print("== Usage ==")
    print("  setmode.py [-hv] [--mode=<mode> --power=<power> --port=<port>]")
    print("")
    print("== Flags ==")
    print("  -h   Print this text")
    print("  -v   Show version number")
    print("")
    print("== Modes ==")
    print("  0 – Packet receive (default)")
    print("  1 - Transparent receive")
    print("  2 - Continous transmit")
    print("")
    print("== Power==")
    print("  Enter power in dBm")
    print("  Integer in range -16 to 6, inclusive")
    print("")
    print("== Example ==")
    print("To transmit continously at full power:")
    print("  setmode.py --mode=2 --power=6 --port=/dev/ttyUSB0")
    print("")


def write_to_radio(radio: Serial, data: bytes):
    out = FEND + escape_special_codes(data) + FEND
    print("Writing bytes to radio:")
    print(bytes_to_str(out))
    radio.write(out)


def print_response(radio: Serial) -> None:
    print("Response from radio:")
    print(bytes_to_str(radio.readall()))


def tcp_listener(radio: Serial) -> None:
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((TCP_ADDR, TCP_PORT))
    s.listen(1)
    print("Listening on TCP port " + TCP_PORT)
    conn, addr = s.accept()
    print("Client connected: " + addr)
    data = conn.recv(BUFFER_SIZE)
    print("Received data: " + bytes_to_str(data))
    write_to_radio(radio, b'\x00' + data)
    print("TCP server done")
    s.close()


def main(argv):
    mode = 0
    power = -16
    port = ""
    server: bool = False

    try:
        opts, args = getopt.getopt(argv,
                                   "h:v:s:",
                                   ["mode=",
                                    "power=",
                                    "port=",
                                    "server",
                                    ])

    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            help()
            sys.exit()

        elif opt == "-v":
            print(VERSION)
            sys.exit()

        elif opt == "--server":
            server = True

        elif opt == "--mode":
            mode = int(arg)

        elif opt == "--power":
            power = int(arg)

        elif opt == "--port":
            port = arg

    if port == "":
        print("Enter a valid serial device with --port=<port>")
        sys.exit(1)

    if mode < 0 or mode > 2:
        print("Invalid mode")
        sys.exit(1)

    if power < -16 or power > 6:
        print("Power out of range (-16 to 6)")
        sys.exit(1)

    radio = get_serialdevice(port)

    print("Setting mode=" + str(mode) + ", power=" + str(power))

    write_to_radio(radio, SET_MODE + int8(mode))
    write_to_radio(radio, SET_POWER + int8(power))

    print_response(radio)

    if server:
        tcp_listener(radio)

    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
