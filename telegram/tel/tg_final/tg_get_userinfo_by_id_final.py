#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/9/12 9:57
# @Author: weifulong
# @File  : config.py
# coding=utf-8
import json
import time
import os
from telethon.tl import functions
from telethon.tl.types import PeerChannel, PeerUser

from telegram.tel.tg_final import client_config


#file_local:文件生成位置,
#file_to_read：需要读取的文件
import eventlet
eventlet.monkey_patch()


async def getUserInfo_byId(client,file_to_read,file_local):
    tg_u = []
    temp_u = []  # 只存 用户id,方便去重
    msg_part_num = 0
    # print('file_to_read',file_to_read,'file_local',file_local)
    try:
        with open(file_to_read,'r',encoding='utf-8') as load_f:
            tg_user = json.load(load_f)
            for i in range(0, len(tg_user)):
                temp_u.append(tg_user[i]['发言者ID：'])
                # tg_u_dict[tg_user[i]['发言者ID：']] = i + 1
            temp_u_format = list(set(temp_u))
            print('++++++++++' ,len(temp_u_format))
            # print(temp_u_format)
            # print(tg_u_dict)
            # 获取发言者信息
        try:
            # 打开同目录下的part.json文件
            part_file = os.path.join(os.path.split(file_to_read)[0], 'part.json')
            part_list = []
            with open(part_file, 'r', encoding='utf-8') as f_part:
                group_list = []
                in_group = False
                for line in f_part:
                    line = line.strip()
                    if line[0] == '{':
                        in_group = True
                        continue
                    elif line[0] == '}':
                        j_s = '{' + '\n'.join(group_list) + '}'
                        # print(j_s)
                        part_list.append(json.loads(j_s))
                        group_list = []
                        in_group = False
                    if in_group:
                        group_list.append(line)
                part_user_id = set()
                for item in part_list:
                    if "admin_用户_id：" in item:
                        part_user_id.add(item["admin_用户_id："])
                    elif "用户_id：" in item:
                        part_user_id.add(item["用户_id："])
                    else:
                        pass
            # 取差集
            temp_u_format = set(temp_u_format)
            temp_u_format = list(temp_u_format - part_user_id)
            print('++++++++++', len(temp_u_format))
        except Exception as e:
            print(e)
        # 存放时间戳
        time_list = []
        for i in range(0, len(temp_u_format)):
            time_list.append(time.time())
            tg_user_final = {}
            #print('msg_part---------------->',temp_u_format[i])
            #with eventlet.Timeout(120, False):  # 1500s限制
            try:
                result_msg = await client.get_entity(PeerUser(int("{}".format(temp_u_format[i]))))
                time_list.append(time.time())
                t_1 = time_list[len(time_list) - 1]
                t_2 = time_list[len(time_list) - 2]
                #超过 5 分钟，就自动获取下一个。直到网络稳定后
                if (t_1 != t_2) & ((t_1 - t_2) > 15):
                    if t_1 - t_2 > 1800:
                        print('跳出，此群组')
                        break
                    print('网络耗时：',(t_1 - t_2))
                    # if (time_list[len(time_list) - 1] - time_list[len(time_list) - 2]) > 300:
                    pass
                # print(result_msg)
                tg_user_final['发言者id：'] = str(result_msg.id)
                tg_user_final['发言者first_name：'] = str(result_msg.first_name)
                tg_user_final['发言者last_name ：'] = str(result_msg.last_name)
                tg_user_final['发言者username ：'] = str(result_msg.username)
                tg_user_final['发言者phone ：'] = str(result_msg.phone)
                # print('tg_user_final[i]',tg_user_final)
                if t_1 != t_2:
                    if i%100 == 0:
                        print('获取msg_part【{}】人'.format(i))
                tg_u.append(tg_user_final)
                # print('tg_u----->', tg_u)
            except Exception as e:
                print('tg_u----->',e.args)
                pass
        # print('tg_u----->', tg_u)
        try:
            with open(file_local, 'w', encoding='utf-8') as f:
                json.dump(tg_u, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("写入by_id：", e.args)
    except Exception as e:
        print('file_to_read', e.args)
        raise e
# s = time.time().

# with client:
#     client.loop.run_until_complete(main())
# print(time.time()-s)
# button_getUserInfo_byId(msg_file_local)