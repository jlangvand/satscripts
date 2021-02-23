# Copyright (C) 2021 Orbit NTNU

# Authors:
# David Ferenc Bendiksen
# Joakim Skogø Langvand
# Sander Aakerholt

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

import re


def bytes_to_str(bytes_in: bytes) -> str:
    """
    Takes bytes as argument and returns a human readable hex string.
    """
    tmp = bytes_in.hex().upper()
    return str.join(" ", list(filter(None, re.split(r'(.{2})', tmp))))


def uint32_to_bytes(i: int, endian: str = "little") -> bytes:
    """
    Return the int as 4 bytes, unsigned, with given endianness (default little)
    """
    return int.to_bytes(i, length=4, byteorder=endian)


def uint16_to_bytes(i: int, endian: str = "little") -> bytes:
    """
    Return the int as 2 bytes, unsigned, with given endianness (default little)
    """
    return int.to_bytes(i, length=2, byteorder=endian)


def uint8_to_bytes(i: int, endian: str = "little") -> bytes:
    """
    Return the int as 1 byte, unsigned
    """
    return int.to_bytes(i, length=1, byteorder=endian)


def bytes_to_int(b: bytes, endian: str = "little") -> bytes:
    """
    Return signed integer with given endianness (default little)
    """
    return int.from_bytes(b, signed=True, byteorder=endian)


def bytes_to_uint(b: bytes, endian: str = "little") -> bytes:
    """
    Return unsigned integer with given endianness (default little)
    """
    return int.from_bytes(b, signed=False, byteorder=endian)


def encode_freq(freq: float) -> bytes:
    """
    Takes frequency in MHz as argument and returns frequency as bytes
    """
    return uint32_to_bytes(int(freq * 10e5), endian="big")


def decode_freq(freq: bytes) -> float:
    """
    Returns frequency in MHz as float
    """
    return int.from_bytes(freq, byteorder="big", signed=False)


def tests():
    """
    Test utils. To be implemented as unit tests.
    """
    print(f"435.000 as bytes: {bytes_to_str(encode_freq(435.000))}")
