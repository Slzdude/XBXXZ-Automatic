# coding:utf-8
import time

from DataMapping.LingGenBase import linggen_base
from data import FRONT_XBXXZ
from xbxxz import *


class UserSystem:
    def __init__(self, client):
        self.client = client
        self.user = t_MainUserProto()

    def init_user(self, user):
        assert isinstance(user, t_MainUserProto)
        self.user = user

    def update_spirit(self, spirit):
        assert isinstance(spirit, t_SpiritNumMessage_XBXXZ)
        assert self.user
        self.user.spiritnum_xxz = spirit.curspirit_xxz

    def update_exp(self, exp):
        assert isinstance(exp, t_AddExpMessage_XBXXZ)
        assert self.user
        self.user.exp_xxz = exp.userexp_xxz

    def update_cave(self, cave):
        assert isinstance(cave, t_CaveValue5SecMessage_XBXXZ)
        assert self.user
        self.user.food_xxz = cave.food_xxz
        self.user.wood_xxz = cave.wood_xxz
        self.user.drug_xxz = cave.drug_xxz
        self.user.iron_xxz = cave.iron_xxz

    def upgrade_linggen(self):
        assert self.user
        linggen = [self.user.goldspiritlevel_xxz, self.user.woodspiritlevel_xxz, self.user.waterspiritlevel_xxz, self.user.firespiritlevel_xxz, self.user.mudspiritlevel_xxz]
        aim_level = min(linggen)
        aim_type = linggen.index(aim_level) + 1

        # aim_level = self.user.waterspiritlevel_xxz
        # aim_type = 3
        if not linggen_base.get(aim_level):
            return False
        min_next_level = int(linggen_base.get(aim_level)['next_XBXXZ'])
        if min_next_level < self.user.maxspiritnum_xxz:
            if self.user.spiritnum_xxz >= min_next_level:
                print('LINGGEN LEVEL UP', aim_level)
                tmp = t_UpLinGenMessage_XBXXZ()
                tmp.type_xxz = aim_type
                self.client.write(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_LINGENUPLEVEL, tmp)
            return True
        return False

    def print(self):
        assert self.user
        print(time.strftime('%H:%M:%S', time.localtime(time.time())), '灵气', self.user.spiritnum_xxz, self.user.maxspiritnum_xxz, '洞府', self.user.food_xxz, self.user.wood_xxz, self.user.drug_xxz,
              self.user.iron_xxz,
              [self.user.goldspiritlevel_xxz, self.user.woodspiritlevel_xxz, self.user.waterspiritlevel_xxz, self.user.firespiritlevel_xxz, self.user.mudspiritlevel_xxz])

    def print2(self):
        assert self.user
        print(
            time.strftime('%H:%M:%S', time.localtime(time.time())),
            '灵石：%d, 声望：%d, 灵气：%d / %d, 草药：%d, 矿石：%d, 进图次数：%d/%d' % (
                self.user.spiritstone_xxz, self.user.reputation_xxz, self.user.spiritnum_xxz, self.user.maxspiritnum_xxz, self.user.drug_xxz, self.user.iron_xxz,
                self.client.enter_info.totalentertimes_xxz, self.client.enter_info.maxturntimes_xxz
            )
        )
