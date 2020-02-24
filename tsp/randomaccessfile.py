import  io
import struct
class randomaccessfile:

    def __init__(self, path, op = None):
        ## todo may cause bug here
        if op == None:
            self.fd = open(path, "r+")
        else:
            self.fd = open(path, op)

    def readint(self, offset):
        assert offset >= 0
        self.fd.seek(offset)
        bytes = self.fd.read(4)
        val = struct.unpack(">i", bytes)

        return val[0]

    def readlong(self, offset):
        assert  offset >= 0
        self.fd.seek(offset)

        bytes = self.fd.read(8)
        if len(bytes) != 8:
            print("bug")
        val = struct.unpack(">q", bytes)

        return val[0]

    def get_last_offset(self):
        self.fd.seek(0, io.SEEK_END)
        last_pos = self.fd.tell()
        return last_pos

    def writeint(self, val, offset = None):
        if val == None:
            val = -1
        if offset == None:
            self.fd.seek(0, io.SEEK_END)
        else:
            self.fd.seek(offset)
        val_bytes = struct.pack(">i", val)
        assert len(val_bytes) == 4
        self.fd.write(val_bytes)

    def writelong(self, val, offset = None):
        if val == None:
            val = -1
        if offset == None:
            self.fd.seek(0, io.SEEK_END)
        else:
            self.fd.seek(offset)

        val_bytes = struct.pack(">q", val)
        assert len(val_bytes) == 8
        self.fd.write(val_bytes)

    def append(self, value):
        self.fd.seek(0, io.SEEK_END)
        self.fd.write(value)

    def write(self, val, offset):
        self.fd.seek(offset)
        self.fd.write(val)

    def read(self, offset, len):
        assert offset >= 0
        assert  len >= 0
        self.fd.seek(offset)
        bytes = self.fd.read(len)

        return bytes