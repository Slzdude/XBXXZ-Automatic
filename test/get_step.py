# coding:utf-8
from xbxxz import stClientUnityMessage_XBXXZ
from xbxxz.data_pb2 import t_MoveMapMessage_XBXXZ
from io import BytesIO

a = open('steps').read().splitlines()
for i in a:
    t = stClientUnityMessage_XBXXZ().Deserialize(BytesIO(bytes.fromhex(i)))
    print(t_MoveMapMessage_XBXXZ.FromString(t.data).pos_xxz)
