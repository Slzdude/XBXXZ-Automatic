# coding:utf-8
import hashlib
import socket
import threading
import time
from queue import Queue

from data import XBXXZ_BACK_MESSAGE, FRONT_XBXXZ
from module import MapSystem, ItemSystem
from utils import stop_thread, wrap_data
from xbxxz import *


class NetworkSystem:
    def __init__(self):
        self.client = socket.socket()
        self.thread_recv = None
        self.mHeader = 0
        self.mTargetLength = 4
        self.mMessageQueue = Queue()
        self.mLoggedIn = False
        self.thread_msg = None
        self.mMessage = b''
        self.map = None
        self.bag = None
        self.user = None
        self.enter_info = t_MapEnterInfoMessage_XBXXZ()
        self.server_ready = False
        self.msg_list = {}

    def init(self, map, bag, user):
        assert isinstance(map, MapSystem)
        assert isinstance(bag, ItemSystem)
        self.map = map
        self.bag = bag
        self.user = user

    def send(self, data):
        # print('SEND', data)
        self.client.send(wrap_data(data))

    def write(self, msg_id, proto_data):
        tmp = stClientUnityMessage_XBXXZ()
        tmp.messageid = msg_id
        tmp.data = proto_data.SerializeToString()
        tmp.size = len(tmp.data)
        self.send(tmp.Serialize())

    def send_id(self, msg_id):
        tmp = stClientUnityMessage_XBXXZ()
        tmp.messageid = msg_id
        self.send(tmp.Serialize())

    def read(self):
        if self.mHeader == 0 and len(self.mMessage) == 4:
            self.mHeader = struct.unpack('<i', self.mMessage)[0]
            self.mTargetLength = self.mHeader
            self.mMessage = b''
        else:
            if len(self.mMessage) < self.mTargetLength:
                data = self.client.recv(1)
                self.mMessage += data
            else:
                self.mHeader = 0
                self.mTargetLength = 4
                self.mMessageQueue.put(self.mMessage)
                self.mMessage = b''

    def recv(self):
        time.sleep(5)
        while True:
            if not self.client or self.client._closed:
                print('Waitting For Connection...')
                time.sleep(0.5)
                continue
            try:
                self.read()
            except Exception as e:
                print(self.client)

    def bind(self, msg_id):
        def decorator(f):
            if not isinstance(msg_id, list):
                tmp = [msg_id]
            else:
                tmp = msg_id
            for i in tmp:
                if i not in self.msg_list.keys():
                    self.msg_list[i] = []
                self.msg_list[i].append(f)
                return f

        return decorator

    def handle_msg(self):
        while True:
            data = self.mMessageQueue.get()
            ret = stNullMessage_XBXXZ().Deserialize(BytesIO(data))
            if ret.byCmd == LOGON_USERCMD:
                if ret.byParam == SERVER_RETURN_LOGIN_OK:
                    ret = stServerReturnLoginSuccessCmd().Deserialize(BytesIO(data))
                    print('Connect Login Server Successfully !')
                    self.login_game(ret)
            elif ret.byCmd == MOBILEUNITY_USERCMD:
                if ret.byParam == SEND_UNITY_USERCMD:
                    ret = stSendUnityMessage_XBXXZ().Deserialize(BytesIO(data))
                    if ret.messageid == XBXXZ_BACK_MESSAGE.XBXXZ_BACK_SELECTUSERINFO:
                        print('Return UserInfo')
                        userinfo = t_stUserInfoMessage_XBXXZProto.FromString(ret.data)
                        if userinfo.userset is None or len(userinfo.userset) == 0 or userinfo.userset[0].id == 0:
                            print('User Not Exist, Creation Needed First.')
                            continue
                        # print(userinfo.userset[0])
                        print('Version: %d, UserID: %d, UserName: %s, Level: %d' % (userinfo.version, userinfo.userset[0].id, userinfo.userset[0].name, userinfo.userset[0].level),
                              userinfo.userset[0].mapid)
                        tmp = t_LoginSelectMessage_XBXXZ()
                        tmp.isReconected_xxz = 0
                        self.write(FRONT_XBXXZ.XBXXZ_FRONT_LOGINSELECT, tmp)
                        self.server_ready = True
                    elif ret.messageid == XBXXZ_BACK_MESSAGE.XBXXZ_BACK_ReturnLoginFailed:
                        ret_code = stServerReturnLoginFailedCmd.FromString(ret.data).returncode
                        print('Return Login Failed: Code', ret_code)
                        if ret_code == 6:
                            stop_thread(self.thread_recv)
                            time.sleep(30)
                            self.login_server()
                            self.create_reader()

                    elif ret.messageid in self.msg_list.keys():
                        for func in self.msg_list[ret.messageid]:
                            func(ret.data)
                    else:
                        if XBXXZ_BACK_MESSAGE.value2name(ret.messageid):
                            # print('Receive Msg:', ret.messageid, ret.data, XBXXZ_BACK_MESSAGE.value2name(ret.messageid))
                            pass
                else:
                    print('CLIENT_UNITY_USERCMD')
            else:
                print('Unknown cmd: %d' % ret.byCmd)

    def create_reader(self):
        # self.stop_thread()
        self.thread_recv = threading.Thread(target=self.recv)
        self.thread_recv.setDaemon(True)
        self.thread_recv.start()

    def create_msg_handler(self):
        self.thread_msg = threading.Thread(target=self.handle_msg)
        self.thread_msg.setDaemon(True)
        self.thread_msg.start()

    def stop_thread(self):
        if self.thread_recv is None:
            return
        stop_thread(self.thread_recv)
        if self.thread_msg is None:
            return
        stop_thread(self.thread_msg)

    def login_server(self):
        self.client = socket.socket()

        self.client.connect(('193.112.170.89', 15029))
        self.send(stUserVerifyVerCmd(1999).Serialize())
        login_url = 'appid=&openid=' + open('account').read().splitlines()[0] + '&timestamp=' + str(int(time.time())) + '&platform=local&server_id=14&access_token='

        md5 = hashlib.md5()
        md5.update(('5720902420ca230e3ed4767a06890bdf&' + login_url).encode())
        userRequestLoginCmd = stUserRequestLoginCmd()
        userRequestLoginCmd.SetSid(login_url + '&sign=' + md5.hexdigest().upper())

        self.send(userRequestLoginCmd.Serialize())

    def login_game(self, server):
        if not self.client._closed:
            client = self.client
            self.client = None
            client.close()
        # self.RecreateNetReader_XBXXZ()
        self.client = socket.socket()
        self.client.connect((server.domain, server.port))
        self.send(stUserVerifyVerCmd(1999).Serialize())
        self.send(stPasswdLogonMessage_XBXXZ(server).Serialize())
