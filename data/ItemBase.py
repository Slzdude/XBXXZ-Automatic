# coding:utf-8
from data.Database import Database


class ItemBase(Database):
    def __init__(self):
        super(ItemBase, self).__init__()
        self.name = 'ItemBase.txt'


item_base = ItemBase()
