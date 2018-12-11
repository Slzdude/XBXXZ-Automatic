# coding:utf-8

import json
import threading
import time

from google.protobuf import json_format

from data import map5_xxz, map7_xxz, MapXXZ
from data.BackMessage import XBXXZ_BACK_MESSAGE
from data.FrontMessage import FRONT_XBXXZ
from module import NetworkSystem, MapSystem, ItemSystem, UserSystem, SchoolSystem
from xbxxz import *

net_sys = NetworkSystem()
map_sys = MapSystem(net_sys, map7_xxz)
item_sys = ItemSystem(net_sys)
user_sys = UserSystem(net_sys)
school_sys = SchoolSystem(net_sys)

net_sys.init(map_sys, item_sys, user_sys)  # 加载模块实例

net_sys.create_reader()
net_sys.create_msg_handler()


@net_sys.bind([XBXXZ_BACK_MESSAGE.XBXXZ_BACK_NONE, XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_OTHERDRAGONLOG])
def none(data):
    pass


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_MAPLIST)
def map_list(data):
    tmp = t_MapListMessage_XBXXZ.FromString(data)
    print(tmp.curmapid_xxz)
    if tmp.curmapid_xxz == 1005:
        map_sys.map = map5_xxz
    elif tmp.curmapid_xxz == 1007:
        map_sys.map = map7_xxz
    else:
        print('Unknown MAP')


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_CHAT)
def chat(data):
    tmp = t_stMobileChannelChatMessage_XBXXZProto.FromString(data)
    if '孙纯阳' in tmp.pstrChat_xxz:
        print(tmp.pstrChat_xxz)


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_PACKNUM)
def pack_num(data):
    print('PACKNUM:', t_MainPackNumProto.FromString(data))


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_SPIRITNUM)
def spirit_num(data):
    user_sys.update_spirit(t_SpiritNumMessage_XBXXZ.FromString(data))


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_ADDEXP)
def addexp(data):
    user_sys.update_exp(t_AddExpMessage_XBXXZ.FromString(data))


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_CAVEVALUE5SEC)
def cave_value_5_sec(data):
    user_sys.update_cave(t_CaveValue5SecMessage_XBXXZ.FromString(data))


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_OBJS)
def objs(data):
    item_sys.add_items(t_stAddObjectListUnityMessage_XBXXZProto.FromString(data))


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_REFRESHOBJS)
def refresh_item(data):
    tmp = t_RefreshObjMessage_XBXXZ.FromString(data)
    item_sys.refresh_item(tmp.qwthisid_xxz, tmp.num_xxz)


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_DELOBJS)
def del_obj(data):
    tmp = t_DelObjMessage_XBXXZ.FromString(data)
    item_sys.remove_item(tmp.qwthisid_xxz)


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_MAPENTERINFO)
def map_enter_info(data):
    net_sys.enter_info = t_MapEnterInfoMessage_XBXXZ.FromString(data)
    print(net_sys.enter_info)
    map_sys.in_map = True
    # print('ENTER:', )


def wait_attack(sec):
    time.sleep(sec)
    map_sys.wait = False


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_NPCATTRESULT)
def att_ret(data):
    tmp = t_NpcAttResultMessage_XBXXZ.FromString(data)
    wait_time = min(9, len(tmp.actions_xxz) - 0.5)
    print('Wait For %.1f' % wait_time)
    wait_attack(wait_time)
    if tmp.result_xxz == 0:
        print('被击败了')
        print(json_format.MessageToJson(tmp))
        exit()


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_MAINUSERDATA)
def main_userdata(data):
    user_sys.init_user(t_MainUserProto.FromString(data))

    # print('RECV USERDATA: ', tmp.spiritstone_xxz, tmp.reputation_xxz)


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_ONEMAPINFO)
def one_map_info(data):
    print('MAP INFO')
    tmp = t_OneMapInfoMessage_XBXXZ.FromString(data)
    map_sys.init_map(json.loads(json_format.MessageToJson(tmp)))


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_SCHOOLINFO)
def school_info(data):
    print('School Info')
    tmp = t_SchoolInfoMessage_XBXXZ.FromString(data)
    school_sys.init_data(tmp)


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_UPSKILL)
def back_upskill(data):
    tmp = t_ReturnUpSkillMessage_XBXXZ.FromString(data)
    school_sys.on_upgrade_skill(tmp)


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_AUTOMAPONLINEEND)
def normal_stop(data):
    print('Auto map finished')
    map_sys.is_automap = False


@net_sys.bind(XBXXZ_BACK_MESSAGE.XBXXZ_BACK_FUNCTION_AUTOMAPRESULT)
def auto_result(data):
    tmp = t_AutoMapResultMessage_XBXXZ.FromString(data)
    if not map_sys.is_special(tmp.mapid_xxz):
        map_sys.auto_map = tmp
        map_sys.is_automap = True


def spirit_monit():
    while True:
        if user_sys.user:
            if user_sys.upgrade_linggen():
                user_sys.print()
            else:
                skills = school_sys.get_scalable_skills(user_sys.user.spiritnum_xxz)
                print('Got %d Scalable Skills' % len(skills), user_sys.user.spiritnum_xxz)
                skill_id = school_sys.get_most_skill(skills)
                if skill_id:
                    school_sys.upgrade_skill(skill_id)
            # socket.send_id(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_JULINUPLEVEL)
        time.sleep(30)


net_sys.login_server()
while not net_sys.server_ready:
    time.sleep(1)


def travel():
    time.sleep(5)
    print('Battle Begin')
    last = user_sys.user.spiritstone_xxz
    while True:
        if not net_sys.client:
            print('Waiting for reconnection')
            time.sleep(3)
        if net_sys.enter_info.maxturntimes_xxz and net_sys.enter_info.totalentertimes_xxz > net_sys.enter_info.maxturntimes_xxz:
            print('暂停过图')
            break
        if not map_sys.map_info:
            if net_sys.enter_info.maxturntimes_xxz:
                if net_sys.enter_info.totalentertimes_xxz <= net_sys.enter_info.maxturntimes_xxz / 2:
                    map_sys.map = map7_xxz
                else:
                    map_sys.map = map5_xxz
            print('Not in map ', map_sys.map.map_id)
            map_sys.enter()
            time.sleep(1)
            continue
        item_sys.handle_all_items()
        if False:
            cur_pos = map_sys.map.cur_pos
            map_sys.map.show()
            cmd = input()
            if cmd[0].upper() == 'C':
                break
            if cmd[0].upper() == 'Q' and map_sys.map.is_exit():
                # print('EXIT_MAP')
                map_sys.exit()
            _step = 1
            if len(cmd) > 1 and cmd[1].isdigit():
                _step = int(cmd[1])
            for _ in range(_step):
                if cmd[0].upper() == 'L':
                    cur_pos -= 1
                if cmd[0].upper() == 'R':
                    cur_pos += 1
                if cmd[0].upper() == 'U':
                    cur_pos -= 20
                if cmd[0].upper() == 'D':
                    cur_pos += 20
                map_sys.move_to(cur_pos)
                if map_sys.map.is_enemy():
                    map_sys.attack()
                    i = 0
                    while map_sys.wait and i < 20:
                        time.sleep(0.5)
                        i += 1
                        map_sys.wait = False
                if map_sys.map.is_entry():
                    map_sys.map_info = False
                time.sleep(0.5)

        else:
            if not map_sys.move():
                item_sys.print_items()
                user_sys.print2()
                print('花费：', map_sys.map.cost, '收入：', user_sys.user.spiritstone_xxz - last)
                last = user_sys.user.spiritstone_xxz
                time.sleep(0.5)
            else:
                time.sleep(0.5)
            # map_sys.map.show()


def auto_map():
    time.sleep(5)
    print('Automap Begin')
    while True:
        if not net_sys.client:
            print('Waiting for connection')
            time.sleep(10)
        if not map_sys.auto_map:
            print('Waiting for auto map message')
            time.sleep(1)
            continue
        if net_sys.enter_info.maxturntimes_xxz and net_sys.enter_info.totalentertimes_xxz > net_sys.enter_info.maxturntimes_xxz:
            print('暂停过图')
            break
        item_sys.handle_all_items()
        auto_map_id = 1026
        if net_sys.enter_info.maxturntimes_xxz:
            if net_sys.enter_info.totalentertimes_xxz <= net_sys.enter_info.maxturntimes_xxz / 2:
                auto_map_id = 1026
            else:
                auto_map_id = 1007
        count = min(net_sys.enter_info.maxautotimes_xxz, int(net_sys.enter_info.maxturntimes_xxz - net_sys.enter_info.totalentertimes_xxz))
        if not count:
            break

        interval = map_sys.auto_map.internaltime_xxz
        if map_sys.auto_map.subhalfsecflag_xxz == 1:
            interval = interval - 0.5

        endtime = map_sys.auto_map.starttime_xxz + map_sys.auto_map.endtime_xxz * interval
        if not map_sys.is_automap or int(time.time()) >= endtime:
            print('Start map %d %d' % (auto_map_id, count))
            net_sys.write(FRONT_XBXXZ.XBXXZ_FRONT_FUNCTION_AUTOMAP, t_ReqAutoMapMessage_XBXXZ(mapid_xxz=auto_map_id, count_xxz=count))
        print('In map %d, running %d/%d, from %s to %s' % (
            map_sys.auto_map.mapid_xxz, map_sys.auto_map.curcount_xxz, map_sys.auto_map.totalcount_xxz, time.strftime("%H:%M:%S", time.localtime(map_sys.auto_map.starttime_xxz)),
            time.strftime("%H:%M:%S", time.localtime(endtime))))
        time.sleep(5)
    print('Finished')


spirit_monit_thread = threading.Thread(target=spirit_monit)
spirit_monit_thread.setDaemon(True)
spirit_monit_thread.start()

auto_map()
# travel()
# time.sleep(3)

while True:
    item_sys.print_items()
    data = input('CMD: ')
    if len(data):
        if data[0].upper() == 'S':
            oid = int(data[1:])
            item_sys.sell_item_id(oid, 0xFFFFFFFF)
