# coding:utf-8
from xbxxz.stMobileUnityMessage_XBXXZ import *


class stSendUnityMessage_XBXXZ(stMobileUnityMessage_XBXXZ):
    def __init__(self):
        super(stSendUnityMessage_XBXXZ, self).__init__()
        self.byParam = SEND_UNITY_USERCMD
        self.messageid = 0
        self.size = 0
        self.data = ''

    def Serialize(self, stream=BytesIO()):
        super(stSendUnityMessage_XBXXZ, self).Serialize(stream)
        stream.write(struct.pack('<II', self.messageid, self.size))
        if isinstance(self.data, bytes):
            stream.write(self.data)
        else:
            stream.write(self.data.encode())
        return stream.getvalue()

    def Deserialize(self, stream=BytesIO()):
        super(stSendUnityMessage_XBXXZ, self).Deserialize(stream)
        self.messageid, self.size = struct.unpack('<II', stream.read(8))
        self.data = stream.read(self.size)
        return self
