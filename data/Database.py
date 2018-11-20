# coding:utf-8
import os


class Database:
    def __init__(self):
        self.name = ''
        self.asset_base = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../assets')
        self.data = {}

    def init_data(self):
        if not self.name:
            return
        data = open(os.path.join(self.asset_base, self.name), 'rb').read().decode().splitlines()
        head = data[0].split('\t')
        del data[0]
        for i in data:
            if len(i) < 2 or i.startswith('//'):
                continue
            item = i.split('\t')
            self.data[int(item[0])] = dict(zip(head, item))

    def get(self, id):
        if not self.data:
            self.init_data()
        if id not in self.data.keys():
            return None
        return self.data[id]
