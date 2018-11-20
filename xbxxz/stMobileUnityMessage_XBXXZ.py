# coding:utf-8
from xbxxz.stNullMessage_XBXXZ import *

SEND_UNITY_USERCMD = 1
CLIENT_UNITY_USERCMD = 2


class stMobileUnityMessage_XBXXZ(stNullMessage_XBXXZ):
    def __init__(self):
        super(stMobileUnityMessage_XBXXZ, self).__init__()
        self.byCmd = MOBILEUNITY_USERCMD

    def Serialize(self, stream=BytesIO()):
        super(stMobileUnityMessage_XBXXZ, self).Serialize(stream)
        return stream.getvalue()

    def Deserialize(self, stream=BytesIO()):
        super(stMobileUnityMessage_XBXXZ, self).Deserialize(stream)
        return self
