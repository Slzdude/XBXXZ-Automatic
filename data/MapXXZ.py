# coding:utf-8
import json
import time
from queue import Queue
import json
from data.TerrainCellType import TerrainCellType_XBXXZ


class MapXXZ:
    def __init__(self, map_id, steps=list()):
        self.map_id = map_id
        self.steps = steps
        self.events = None
        self.cur_pos = 0
        self.last_pos = 0
        self.step_index = 0

        self.cost = len(steps) * (map_id - 1000)

    def init_map(self, map_data):
        # open('map/%d.json' % self.map_id, 'w').write(json.dumps(map_data))
        self.events = map_data['eventsXxz']
        self.cur_pos = map_data['curposXxz']
        print(self.cur_pos)
        self.step_index = 0
        self.last_pos = map_data['lastposXxz']

        # open('map5', 'w').write(json.dumps(map_data))

    @staticmethod
    def rindex(ls, target):
        for i in range(len(ls)):
            if ls[len(ls) - i - 1] == target:
                return len(ls) - i - 1
        return -1

    def get_step(self):
        cur_pos = self.cur_pos
        if cur_pos not in self.steps:
            self.step_index = 0
        if not self.step_index:
            self.step_index = self.rindex(self.steps, self.cur_pos)

        self.step_index += 1
        step = self.steps[self.step_index]
        self.cur_pos = step
        return step

    def is_exit(self):  # 判断是否为出口
        # and self.step_index == len(self.steps) - 1
        return TerrainCellType_XBXXZ(self.events[self.cur_pos - 1]['typeXxz']) == TerrainCellType_XBXXZ.NextMap

    def is_enemy(self):  # 判断是否为可攻击目标
        return self.events[self.cur_pos - 1]['typeXxz'] in [5, 7, 13, 14, 15]

    def show(self, pos=0, val=''):
        i = 1
        line = '|'
        for event in self.events:
            evt_type = TerrainCellType_XBXXZ(event['typeXxz'])
            if evt_type == TerrainCellType_XBXXZ.Empty:
                tmp = ' ' * 12
            elif evt_type == TerrainCellType_XBXXZ.Block:
                tmp = 'X' * 12
            elif evt_type == TerrainCellType_XBXXZ.Chest:
                tmp = '%-12s' % ('%dX%d' % (event['value1Xxz'], event['value2Xxz']))
            else:
                tmp = '%-12s' % evt_type.name
                # line += '%02d' % evt_type
            if self.cur_pos == i:
                tmp = '%-12s' % 'curpos'
            if event['posXxz'] == pos:
                tmp = val
            line += tmp
            if i % 20 == 0:
                print(line + '|')
                line = '|'
            else:
                line += '|'
            i += 1

    def interactive(self):
        cmd_list = [self.cur_pos]
        while True:
            self.show()
            cmd = input()
            if len(cmd.strip()) == 0 or cmd[0].upper() not in 'QLRUD':
                continue
            if cmd[0].upper() == 'Q':
                print(cmd_list)
                exit()
            count = 1
            if len(cmd) > 1:
                count = int(cmd[1])
            for _ in range(count):
                if cmd[0].upper() == 'L':
                    self.cur_pos -= 1
                if cmd[0].upper() == 'R':
                    self.cur_pos += 1
                if cmd[0].upper() == 'U':
                    self.cur_pos -= 20
                if cmd[0].upper() == 'D':
                    self.cur_pos += 20
                cmd_list.append(self.cur_pos)

    def show_steps(self):
        for i in range(len(self.steps) - 1):
            self.get_step()
            val = 'O' * 12
            tmp = self.steps[i + 1] - self.steps[i]
            if tmp == -20:
                val = '↑' * 6
            if tmp == 20:
                val = '↓' * 6
            if tmp == -1:
                val = '←' * 6
            if tmp == 1:
                val = '→' * 6
            self.show(self.steps[i], val)
            time.sleep(0.5)


map1_xxz = MapXXZ(1001, [
    390, 389, 388, 387, 367, 347,
    327, 307, 287, 267, 247,
    227, 207, 187, 167, 168,
    169, 170, 171, 151, 131,
    111, 91, 71, 51, 31, 11,
    10, 9, 8, 7, 27, 26, 46,
    66, 86, 106, 105, 104, 103,
    102, 82, 62, 42, 41, 21,
    22, 2, 1
])

map2_xxz = MapXXZ(1002, [
    384, 385, 386, 387, 367,
    347, 327, 328, 308, 309,
    310, 290, 270, 250, 230,
    231, 211, 191, 171, 151,
    131, 111, 91, 71, 51,
    31, 11, 10, 9, 8,
    7, 27, 47, 46, 66,
    86, 85, 105, 104, 103,
    102, 101, 81, 61, 41,
    21, 1, 2, 22, 42
])

# [
#     300, 299, 298, 297, 277,
#     257, 258, 259, 239, 219,
#     218, 217, 216, 215, 214,
#     213, 212, 211, 191, 171,
#     151, 131, 111, 91, 71,
#     51, 31, 11, 10, 9,
#     8, 7, 6, 5, 4,
#     3, 2, 1, 21, 22,
#     42, 43, 44, 45, 46,
#     66, 86, 106, 105, 104,
#     124, 144, 164, 163, 183,
#     203, 202, 201, 221, 241,
#     261, 281, 301, 321, 341,
#     361, 362, 382, 381
# ]

map3_xxz = MapXXZ(1003, [
    300, 299, 298, 297, 277,
    257, 258, 259, 239, 219,
    218, 217, 216, 215, 195,
    175, 155, 135, 115, 95,
    75, 76, 77, 57, 37,
    17, 18, 19, 39, 40,
    60, 80, 79, 99, 100,
    80, 60, 40, 20, 19,
    18, 17, 16, 15, 14,
    13, 12, 11, 10, 9,
    8, 28, 48, 47, 46,
    66, 86, 106, 105, 85,
    65, 45, 44, 43, 42,
    22, 2, 1, 21, 41,
    61, 81, 101, 102, 103,
    104, 124, 144, 164, 163,
    162, 182, 202, 201, 221,
    241, 261, 281, 301, 321,
    341, 361, 362, 382, 381
])

map4_xxz = MapXXZ(1004, [
    382, 381, 361, 341, 321,
    301, 281, 261, 241, 221,
    201, 202, 203, 204, 205,
    225, 245, 265, 285, 305,
    325, 345, 346, 347, 348,
    349, 350, 351, 352, 353,
    354, 355, 375, 395, 396,
    397, 377, 378, 379, 380,
    400, 380, 360, 340, 320,
    319, 299, 279, 259, 239,
    219, 199, 179, 178, 177,
    176, 175, 174, 173, 172,
    171, 170, 169, 168, 167,
    166, 165, 164, 144, 124,
    104, 103, 102, 101, 102,
    103, 104, 105, 85, 86,
    106, 126, 127, 128, 108,
    88, 68, 48, 28, 8,
    7, 27, 26, 46, 45,
    44, 43, 42, 41, 21,
    22, 23, 3, 2, 1
])

map5_xxz = MapXXZ(1005, [
    381, 382, 383, 384, 385,
    386, 387, 388, 368, 348,
    347, 346, 345, 344, 343,
    342, 341, 321, 301, 302,
    282, 283, 263, 243, 223,
    203, 183, 163, 164, 165,
    164, 144, 124, 104, 103,
    102, 101, 81, 61, 41,
    21, 1, 2, 3, 23,
    22, 42, 43, 44, 45,
    65, 85, 105, 106, 86,
    66, 46, 26, 27, 28,
    48, 28, 8, 9, 10,
    11, 31, 51, 71, 91,
    90, 91, 92, 91, 111,
    131, 130, 150, 170, 190,
    210, 230, 229, 230, 250,
    230, 231, 232, 233, 234,
    235, 236, 216, 215, 195,
    175, 155, 135, 136, 137,
    117, 97, 77, 57, 37,
    17, 18, 19, 39, 40,
    20, 40, 60, 80
])

map7_xxz = MapXXZ(1007, [
    381, 361, 341, 342, 341,
    321, 301, 281, 282, 283,
    284, 285, 305, 306, 307,
    308, 309, 310, 311, 312,
    313, 314, 294, 274, 254,
    234, 214, 215, 216, 217,
    197, 177, 157, 158, 159,
    160, 140, 120, 100, 99,
    79, 80, 60, 40, 39,
    19, 18, 17, 37, 57,
    77, 76, 75, 74, 94,
    114, 113, 112, 111, 110,
    90, 91, 92, 72, 71,
    51, 31, 11, 10, 9,
    8, 7, 27, 28, 48,
    47, 46, 66, 86, 106,
    105, 85, 65, 45, 44,
    43, 23, 3, 2, 22,
    42, 41, 21, 1
])

map6_xxz = MapXXZ(1006, [
    220, 219, 218, 217, 237,
    257, 277, 297, 317, 316,
    315, 314, 294, 274, 254,
    234, 214, 215, 195, 175,
    155, 135, 115, 114, 113,
    112, 111, 110, 90, 91,
    92, 72, 71, 51, 31,
    11, 10, 9, 8, 7,
    27, 28, 48, 47, 46,
    66, 86, 106, 105, 104,
    124, 144, 164, 165, 166,
    167, 168, 167, 187, 207,
    227, 247, 267, 287, 307,
    327, 347, 367, 387, 386,
    385, 365, 345, 325, 305,
    304, 303, 283, 263, 243,
    223, 203, 202, 222, 242,
    241, 261, 281, 301, 321,
    341, 342, 341, 361, 362,
    382, 381
])
map2001_xxz = MapXXZ(2001, [
    391, 390, 389, 388, 387,
    386, 385, 384, 383, 382,
    381, 361, 341, 342, 362,
    363, 343, 344, 364, 365,
    345, 346, 366, 367, 347,
    348, 368, 369, 349, 350,
    370, 371, 372, 392, 393,
    373, 374, 394, 395, 375,
    376, 396, 397, 377, 378,
    398, 399, 379, 380, 400,
    380, 360, 359, 358, 357,
    356, 355, 354, 353, 352,
    351, 331, 311, 310, 309,
    308, 307, 306, 305, 304,
    303, 302, 301, 281, 282,
    283, 284, 285, 286, 287,
    288, 289, 290, 291, 292,
    312, 313, 314, 315, 316,
    317, 318, 298, 299, 300,
    280, 300, 320, 300, 299,
    298, 297, 296, 295, 294,
    293, 292, 291, 271, 270,
    269, 268, 267, 266, 265,
    264, 263, 262, 261, 262,
    263, 264, 265, 266, 267,
    268, 269, 270, 271, 272,
    273, 274, 275, 276, 277,
    278, 277, 276, 275, 274,
    273, 272, 271, 270, 269,
    270, 271, 251, 231, 230,
    229, 228, 227, 226, 225,
    224, 223, 203, 204, 205,
    206, 207, 208, 209, 210,
    211, 212, 213, 214, 215,
    216, 217, 218, 238, 237,
    236, 235, 234, 233, 232,
    231, 211, 191, 190, 189,
    188, 187, 186, 185, 184,
    183, 184, 185, 186, 187,
    188, 189, 190, 191, 192,
    193, 194, 195, 196, 197,
    198, 218, 219, 220, 200
])
if __name__ == '__main__':
    data = json.loads(open('../data/1007.json').read())
    map7_xxz.init_map(data)
    map7_xxz.show_steps()
