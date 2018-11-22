# coding:utf-8
import json
import time

from data import FRONT_XBXXZ, MapXXZ
from xbxxz import t_EnterMapMessage_XBXXZ, t_MoveMapMessage_XBXXZ


class MapSystem:
    def __init__(self, client, cur_map):
        assert isinstance(cur_map, MapXXZ)
        self.client = client
        self.map = cur_map
        self.wait = False
        self.map_info = False
        self.in_map = False

    def init_map(self, data):
        self.map.init_map(data)
        self.map_info = True
        self.wait = False
        if self.is_enemy():
            self.attack()

    def move(self):
        next_step = self.map.get_step()
        print('Move to:', next_step)
        self.move_to(next_step)
        if self.map.is_enemy():
            time.sleep(2)
            self.attack()
            i = 0
            while self.wait and i < 20:
                time.sleep(0.5)
                i += 1
            self.wait = False
        if self.map.is_exit():
            # print('EXIT_MAP')
            self.exit()
            return False
        return True

    def move_to(self, next_step):
        tmp = t_MoveMapMessage_XBXXZ()
        tmp.pos_xxz = next_step
        tmp.SerializeToString()
        self.client.write(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_MOVEMAP, tmp)
        self.map.cur_pos = next_step

    def enter(self):
        tmp = t_EnterMapMessage_XBXXZ()
        tmp.mapid_xxz = self.map.map_id
        self.client.write(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_ENTERMAP, tmp)

    def exit(self):
        self.in_map = False
        self.map_info = False
        self.client.send_id(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_RETREAT)

    def attack(self):
        self.client.send_id(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_NPCATT)
        self.wait = True

    def is_enemy(self):
        return self.map.is_enemy()
