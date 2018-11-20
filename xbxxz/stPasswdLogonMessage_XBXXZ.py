# coding:utf-8

from xbxxz.stLogonMessage_XBXXZ import *


class stPasswdLogonMessage_XBXXZ(stLogonMessage_XBXXZ):
    def __init__(self, server):
        super(stPasswdLogonMessage_XBXXZ, self).__init__()
        self.pstrName = ''
        self.pstrPassword = ''
        self.loginTempID = server.loginTempID
        self.dwUserID = server.dwUserID
        self.byParam = PASSWD_LOGON_USERCMD_PARA

    def Serialize(self, stream=BytesIO()):
        super(stPasswdLogonMessage_XBXXZ, self).Serialize(stream)
        stream.write(struct.pack('<IQ48s16s', self.loginTempID, self.dwUserID, self.pstrName.encode(), self.pstrPassword.encode()))
        return stream.getvalue()

    def Deserialize(self, stream):
        super(stPasswdLogonMessage_XBXXZ, self).Deserialize(stream)
        self.loginTempID, self.dwUserID, self.pstrName, self.pstrPassword = struct.unpack('<IQ48s16s', stream.read(76))
        return self
