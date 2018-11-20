# coding:utf-8
import json
from data.TerrainCellType import TerrainCellType_XBXXZ


class Map:
    def __init__(self, data):
        self.events = data['eventsXxz']
        self.curpos = data['curposXxz']
        self.lastpos = data['lastposXxz']

    def Show(self):
        i = 1
        line = '|'
        for event in self.events:
            tmp = ''
            evt_type = TerrainCellType_XBXXZ(event['typeXxz'])
            if evt_type == TerrainCellType_XBXXZ.Empty:
                tmp = ' ' * 10
            elif evt_type == TerrainCellType_XBXXZ.Block:
                tmp = 'X' * 10
            elif evt_type == TerrainCellType_XBXXZ.Chest:
                tmp = '%-10s' % ('%dX%d' % (event['value1Xxz'], event['value2Xxz']))
            else:
                tmp = '%-10s' % evt_type.name
                # line += '%02d' % evt_type
            if self.curpos == i:
                tmp = 'curpos    '
            if self.lastpos == i:
                tmp = 'lastpos   '

            line += tmp
            if i % 20 == 0:
                print(line + '|')
                line = '|'
            else:
                line += '|'
            i += 1

    def IsEnemy(self):
        return self.events[self.curpos - 1]['typeXxz'] in [5, 7, 13, 14, 15]

    def NextStep(self):
        cur = self.curpos
        steps = [
            390, 389, 388, 387, 367, 347,
            327, 307, 287, 267, 247,
            227, 207, 187, 167, 168,
            169, 170, 171, 151, 131,
            111, 91, 71, 51, 31, 11,
            10, 9, 8, 7, 27, 26, 46,
            66, 86, 106, 105, 104, 103,
            102, 82, 62, 42, 41, 21,
            22, 2, 1
        ]
        if cur not in steps or steps[-1] == cur:
            return None
        self.curpos = steps[steps.index(cur) + 1]
        return self.curpos

    def interactive(self):
        cmd_list = []
        cmd_list.append(self.curpos)
        while True:
            self.Show()
            cmd = input()
            if cmd[0].upper() == 'Q':
                print(cmd_list)
                exit()
            count = 1
            if len(cmd) > 1 and cmd[1].isdigit():
                count = int(cmd[1])
            for _ in range(count):
                if cmd[0].upper() == 'L':
                    self.curpos -= 1
                if cmd[0].upper() == 'R':
                    self.curpos += 1
                if cmd[0].upper() == 'U':
                    self.curpos -= 20
                if cmd[0].upper() == 'D':
                    self.curpos += 20
                cmd_list.append(self.curpos)


if __name__ == '__main__':
    data = json.loads(open('../data/map3').read())
    Map(data).interactive()
