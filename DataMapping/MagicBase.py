# coding:utf-8
from DataMapping.Database import Database


class MagicBase(Database):
    def __init__(self):
        super(MagicBase, self).__init__()
        self.name = 'MagicBase.txt'


magic_base = MagicBase()
