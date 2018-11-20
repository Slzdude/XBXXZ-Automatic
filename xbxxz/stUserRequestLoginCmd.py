# coding:utf-8

from xbxxz.stLogonMessage_XBXXZ import *


class stUserRequestLoginCmd(stLogonMessage_XBXXZ):
    def __init__(self):
        super(stUserRequestLoginCmd, self).__init__()
        self.byParam = USER_REQUEST_LOGIN_PARA
        self.sid = ''
        self.wdSize = 0  # Short

    def Serialize(self, stream=BytesIO()):
        super(stUserRequestLoginCmd, self).Serialize(stream)
        stream.write(struct.pack('<H', self.wdSize))
        stream.write(self.sid.encode())
        return stream.getvalue()

    def Deserialize(self, stream):
        super(stUserRequestLoginCmd, self).Deserialize(stream)
        self.wdSize = struct.unpack('<H', stream.read(2))[0]
        self.sid = stream.read(self.wdSize)
        return self

    def SetSid(self, sid):
        self.sid = sid
        self.wdSize = len(sid)
