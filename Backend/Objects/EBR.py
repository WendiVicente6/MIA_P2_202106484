import struct
import random
import ctypes
import datetime

class EBR(ctypes.Structure):
    def __init__(self):
        self.part_status = '0'
        self.part_fit = ''
        self.part_start = 0
        self.part_size = 0
        self.part_next = -1
        self.part_name = ''
    
    def __bytes__(self):
        return (self.part_status.encode('utf-8') +
                self.part_fit.encode('utf-8') +
                struct.pack("<i", self.part_start) +
                struct.pack("<i", self.part_size) +
                struct.pack("<i", self.part_next) +
                self.part_name.encode('utf-8').ljust(16, b'\x00'))

    def __setstate__(self, data):
        self.part_status = data[:1].decode('utf-8')
        self.part_fit = data[1:2].decode('utf-8')
        self.part_start = struct.unpack("<i", data[2:6])[0]
        self.part_size = struct.unpack("<i", data[6:10])[0]
        self.part_next = struct.unpack("<i", data[10:14])[0]
        self.part_name = data[14:30].decode('utf-8').rstrip('\0')