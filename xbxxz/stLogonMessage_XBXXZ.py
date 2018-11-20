# coding:utf-8
from xbxxz.stNullMessage_XBXXZ import *

USER_VERIFY_VER_PARA = 1
USER_REQUEST_LOGIN_PARA = 2
SERVER_RETURN_LOGIN_FAILED = 3
SERVER_RETURN_LOGIN_OK = 4
PASSWD_LOGON_USERCMD_PARA = 5
GM_REQUEST_LOGIN_PARA = 11


class stLogonMessage_XBXXZ(stNullMessage_XBXXZ):
    def __init__(self):
        super(stLogonMessage_XBXXZ, self).__init__()
        self.byCmd = LOGON_USERCMD

    def Serialize(self, stream):
        super(stLogonMessage_XBXXZ, self).Serialize(stream)
        return stream.getvalue()

    def Deserialize(self, stream):
        super(stLogonMessage_XBXXZ, self).Deserialize(stream)
        return self
