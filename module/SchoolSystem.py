# coding:utf-8
from threading import RLock
from data import FRONT_XBXXZ, magic_base
from xbxxz import *


class SchoolSystem:
    def __init__(self, client):
        self.client = client
        self.school = t_SchoolInfoMessage_XBXXZ()

    def init_data(self, data):
        assert isinstance(data, t_SchoolInfoMessage_XBXXZ)
        self.school = data

    def upgrade_skill(self, skill_id):
        tmp = t_UpSkillMessage_XBXXZ()
        tmp.skillid_xxz = skill_id
        self.client.write(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_UPSKILL, tmp)

    def on_upgrade_skill(self, data):
        assert isinstance(data, t_ReturnUpSkillMessage_XBXXZ)
        for i in self.school.skills_xxz:
            if i.skillid_xxz == data.skillid_xxz:
                magic = magic_base.get(data.skillid_xxz)
                print('升级：', magic['ID_XBXXZ'], magic['Name_XBXXZ'], magic['Level_XBXXZ'], magic['Effect_XBXXZ'], '当前等级：', data.skilllevel_xxz)
                i.skilllevel_xxz = data.skilllevel_xxz
                break

    def get_scalable_skills(self, spirit_num):
        level_exp = [100, 5000, 25000, 125000, 625000, 2600000, 7800000, 16000000, 33000000]
        ret = []

        for i in self.school.skills_xxz:
            magic = magic_base.get(i.skillid_xxz)
            if int(magic['LevelLimit_XBXXZ']) <= i.skilllevel_xxz:
                continue
            if level_exp[i.skilllevel_xxz - 1] > spirit_num:
                continue
            ret.append(i)
        return ret

    def get_most_skill(self, skills):
        ret = {}
        if not skills:
            return
        for i in skills:
            assert isinstance(i, t_SchoolSkillProto)
            magic = magic_base.get(i.skillid_xxz)
            rate = int(magic['Level_XBXXZ'])
            ret[i.skillid_xxz] = rate
        ret = sorted(ret.items(), key=lambda d: d[1], reverse=True)
        return ret[0][0]
