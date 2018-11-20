# coding:utf-8

from xbxxz.stLogonMessage_XBXXZ import *


class stServerReturnLoginSuccessCmd(stLogonMessage_XBXXZ):
    def __init__(self):
        super(stServerReturnLoginSuccessCmd, self).__init__()
        self.byParam = SERVER_RETURN_LOGIN_OK
        self.dwUserID = 0
        self.loginTempID = 0
        self.port = 0
        self.domain = ''

    def Serialize(self, stream=BytesIO()):
        super(stServerReturnLoginSuccessCmd, self).Serialize(stream)
        stream.write(struct.pack('<QI65sH', self.dwUserID, self.loginTempID, self.domain.encode(), self.port))
        return stream.getvalue()

    def Deserialize(self, stream):
        super(stServerReturnLoginSuccessCmd, self).Deserialize(stream)
        self.dwUserID, self.loginTempID, self.domain, self.port = struct.unpack('<QI65sH', stream.read(79))
        self.domain = self.domain.decode().strip('\x00')
        return self
