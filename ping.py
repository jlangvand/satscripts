#!/bin/python

import sys
from setup import get_serialdevice, ping


radio = get_serialdevice()

radio.write(ping)

print(radio.read(radio.in_waiting))
