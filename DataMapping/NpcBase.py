# coding:utf-8
from DataMapping.Database import Database


class NpcBase(Database):
    def __init__(self):
        super(NpcBase, self).__init__()
        self.name = 'NpcBase.txt'


npc_base = NpcBase()
