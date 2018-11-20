from enum import Enum


class TerrainCellType_XBXXZ(Enum):
    NAN = 0
    Entry = 1
    Empty = 2
    Block = 3  # 砖块
    Grass = 4  # 药草
    Monster = 5  # 妖族
    Chest = 6  # 宝箱
    Boss = 7  # Boss
    Material = 8  # 玄铁
    SpiritStone = 9  # 灵石
    Formation = 10  # ?
    Servant = 11  # 仆役
    NextMap = 12  # 下张图
    Demon = 13  # 鬼族
    Asmodians = 14  # 恶魔族
    Human = 15  # 人族
    MAP_Monster1 = 16
    MAP_Monster2 = 17
    MAP_Monster3 = 18
    MAP_Stone1 = 19
    MAP_Stone2 = 20
    MAP_Stone3 = 21
    MAP_Wood = 22
