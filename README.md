# setmode.py
Set mode and power output for the Nanoavionics Sat2RF1 satellite radio module.

For testing and debugging purposes.

> Always make sure there's a properly sized 50Ω load connected to the RF output!
____
## Usage
`$ python setmode.py [-h|-v] --mode=<0...2> --power=<-16...6> --port=/path/to/interface

### Mode
0 = Packet receive (default), 1 = Transparent receive, 2 = continuous transmit (beacon).

### Power
Power is given in dBm, in the range -16dBm to 6dBm, inclusive.

## Example
To transmit a beacon at full power with the radio connected through `/dev/ttyUSB0`:

`$ python setmode.py --mode=2 --power=6 --port=/dev/ttyUSB0`