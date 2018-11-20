# coding:utf-8
import struct
from io import BytesIO

MAX_PASSWORD = 16
MAX_NAMESIZE = 64
MAX_DOMAINSIZE = 64
MAX_ACCNAMESIZE = 48
NULL_USERCMD = 0
TIME_USERCMD = 1
LOGON_USERCMD = 2
DATA_USERCMD = 4
MAPSCREEN_USERCMD = 7
SELECT_USERCMD = 19
SCRIPT_USERCMD = 30
MOBILEUNITY_USERCMD = 53


class stNullMessage_XBXXZ:
    def __init__(self):
        self.byCmd = NULL_USERCMD
        self.byParam = 0
        self.dwTimestamp = 0

    def __str__(self):
        return '{ byCmd=%d, byParam=%d, dwTimestamp=%d }' % (self.byCmd, self.byParam, self.dwTimestamp)

    def Serialize(self, stream):
        if not isinstance(stream, BytesIO):
            raise TypeError('Data must convert to BytesIO')
        stream.seek(0)
        stream.write(struct.pack('<bbi', self.byCmd, self.byParam, self.dwTimestamp))
        return stream.getvalue()

    def Deserialize(self, stream):
        if not isinstance(stream, BytesIO):
            raise TypeError('Data must convert to BytesIO')
        stream.seek(0)
        self.byCmd, self.byParam, self.dwTimestamp = struct.unpack('<bbi', stream.read(6))
        return self
