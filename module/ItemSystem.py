# coding:utf-8
from threading import RLock
from google.protobuf import json_format
from data import FRONT_XBXXZ, item_base
from xbxxz import *


class ItemSystem:
    def __init__(self, client):
        self.client = client
        self.lock = RLock()
        self.items = {}

    def handle_item(self, obj):
        assert isinstance(obj, t_ObjectProto)
        item = item_base.get(obj.dwObjectID_xxz)
        if obj.pos_xxz.dwLocation_xxz == 2:
            # print('EQUIP', obj.strName_xxz)
            return
        item_type = int(item['Type_XBXXZ'])

        if obj.dwObjectID_xxz in []:
            return

        if item_type in [11, 12, 13]:
            self.sell_item(obj)

        if obj.dwObjectID_xxz in [1, 2, 3, 4, 5] or 18 < obj.dwObjectID_xxz < 28:
            self.sell_item(obj)
        elif item_type in [5] or obj.dwObjectID_xxz in [38]:
            self.use_item(obj)
        else:
            pass
            # print(obj.strName_xxz)

    def has_item(self, item_id):
        if self.lock.acquire():
            ret = item_id in self.items
            self.lock.release()
            return ret

    def add_item(self, obj):
        assert isinstance(obj, t_ObjectProto)
        if self.lock.acquire():
            if self.has_item(obj.qwThisID_xxz):
                self.refresh_item(obj.qwThisID_xxz, obj.dwNum_xxz)
            else:
                self.items[obj.qwThisID_xxz] = obj
            self.lock.release()

    def add_items(self, objs):
        assert isinstance(objs, t_stAddObjectListUnityMessage_XBXXZProto)
        for i in objs.userset_xxz:
            self.add_item(i.obj_xxz)

    def refresh_item(self, item_id, num):
        if self.lock.acquire():
            if self.has_item(item_id):
                tmp = self.items[item_id]
                tmp.dwNum_xxz = num
                self.items[item_id] = tmp
            self.lock.release()

    def remove_item(self, item_id):
        if self.lock.acquire():
            if not self.has_item(item_id):
                print('ITEM_NOT_EXIST', item_id)
                return
            del self.items[item_id]
            self.lock.release()

    def buy_item(self, item_id, shop_type, num):
        tmp = t_BuyObjMessage_XBXXZ()
        tmp.itemid_xxz = item_id
        tmp.index_xxz = shop_type
        tmp.itemnum_xxz = num
        self.client.write(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_BUYOBJ, tmp)

    def use_item_id(self, item_id, num):
        tmp = t_UserItemMessage_XBXXZ()
        tmp.qwthisid_xxz = item_id
        tmp.num_xxz = num
        self.client.write(FRONT_XBXXZ.XBXXZ_FRONT_USEOBJS, tmp)

    def sell_item_id(self, item_id, num):
        tmp = t_SellObjMessage_XBXXZ()
        tmp.objthisid_xxz = item_id
        tmp.num_xxz = num
        self.client.write(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_SELLOBJ, tmp)

    def sell_item(self, obj):
        assert isinstance(obj, t_ObjectProto)
        # print('SELL', obj.strName_xxz, obj.dwNum_xxz)
        self.sell_item_id(obj.qwThisID_xxz, obj.dwNum_xxz)

    def use_item(self, obj):
        assert isinstance(obj, t_ObjectProto)
        # print('USE', obj.strName_xxz, obj.dwNum_xxz)
        self.use_item_id(obj.qwThisID_xxz, obj.dwNum_xxz)

    def handle_all_items(self):
        if self.lock.acquire():
            for i in self.items.values():
                self.handle_item(i)
            self.lock.release()

    def print_items(self):
        if self.lock.acquire():
            ret = ''
            for i in self.items.values():
                if i.pos_xxz.dwLocation_xxz == 2:
                    # print('EQUIP', obj.strName_xxz)
                    continue
                ret += '%s x%d, ' % (i.strName_xxz, i.dwNum_xxz)
            print(ret, len(self.items))

            self.lock.release()
