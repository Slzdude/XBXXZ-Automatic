# coding:utf-8
from xbxxz.stLogonMessage_XBXXZ import *

USER_VERIFY_VER_PARA = 1
USER_REQUEST_LOGIN_PARA = 2
SERVER_RETURN_LOGIN_FAILED = 3
SERVER_RETURN_LOGIN_OK = 4
PASSWD_LOGON_USERCMD_PARA = 5
GM_REQUEST_LOGIN_PARA = 11


class stUserVerifyVerCmd(stLogonMessage_XBXXZ):
    def __init__(self, version=0):
        super(stUserVerifyVerCmd, self).__init__()
        self.byParam = USER_VERIFY_VER_PARA
        self.reserve = 0
        self.version = version

    def Serialize(self, stream=BytesIO()):
        super(stUserVerifyVerCmd, self).Serialize(stream)
        stream.write(struct.pack('<II', self.reserve, self.version))
        return stream.getvalue()

    def Deserialize(self, stream):
        super(stUserVerifyVerCmd, self).Deserialize(stream)
        self.reserve, self.version = struct.unpack('<II', stream.read(8))
        return self
