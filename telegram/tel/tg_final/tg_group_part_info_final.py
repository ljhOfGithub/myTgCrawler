#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2019/9/12 9:57
#@Author: weifulong
#@File  : test2.py
#coding=utf-8
import json
import time

from telethon.tl.types import PeerUser, PeerChat, PeerChannel,UpdateNewChannelMessage
from telethon.tl.types import ChannelParticipantsAdmins

#存放时间戳
time_list_admin = []
time_list_part = []
time_list_part_w = []

async def tg_get_group_part(client,part_file_local,part_admin_file_local,channel_id,group_num):
    client = client
    result = [] #用于储存json文件
    result_admin = [] #用于储存json文件
    part_admin_num = 0
    #part_num = 0
    # ===============获取admin========
    time_list_admin.append(time.time())
    time_list_admin.append(time.time())
    for user in await client.get_participants(await client.get_entity(PeerChannel(int('{channel_id}'.format(channel_id=channel_id)))),filter=ChannelParticipantsAdmins, aggressive=True):
        time_list_admin.append(time.time())
        t_1 = time_list_admin[len(time_list_admin) - 1]
        t_2 = time_list_admin[len(time_list_admin) - 2]
        if (t_1 != t_2) & ((t_1 - t_2) > 15):
            # if (time_list[len(time_list) - 1] - time_list[len(time_list) - 2]) > 300:
            if t_1 - t_2 > 1800 :
                print("跳出，此群组")
                break
            print('网络耗时：', t_1 - t_2)

        temp_dict = {}
        part_admin_num += 1
        temp_dict['admin_用户_id：'] = str(user.id)
        temp_dict['admin_用户_first_name'] = user.first_name
        temp_dict['admin_用户_last_name'] = user.last_name
        temp_dict['admin_用户名_username'] = user.username
        temp_dict['admin_用户_phone'] = str(user.phone)
        result_admin.append(temp_dict)
    print('===== 获取群管理员结束，总共{}个管理员 ===='.format(part_admin_num))
    # try:
    #     with open('{file_local}'.format(file_local=part_admin_file_local),'w',encoding='utf-8') as f :
    #         json.dump(result_admin,f,ensure_ascii=False,indent=2)
    # except Exception as e:
    #     print(e.args)
    #     pass
        # print(user.stringify())

    # ===============获取群成员信息========
# =========获取用户id 1W+，同时可以获取用户内容==================
    channel =await client.get_entity(PeerChannel(int('{channel_id}'.format(channel_id=channel_id))))  # 根据群组id获取群组对
    part_num = 0
    # channel = '[公海總谷2.0] 五大訴求，缺一不可。'

    if int(group_num) <= 10000:
        time_list_part.append(time.time())
        time_list_part.append(time.time())
        async for ip in client.iter_participants(channel):
            part_num += 1
            if (part_num % 100) == 0:
                time_list_part.append(time.time())
                print('获取了【{}】个用户'.format(part_num),'channel_id',channel_id)
            t_1 = time_list_part[len(time_list_part) - 1]
            t_2 = time_list_part[len(time_list_part) - 2]
            if (t_1 != t_2) & ((t_1 - t_2) > 15):
                # if (time_list[len(time_list) - 1] - time_list[len(time_list) - 2]) > 300:
                #print('网络耗时：', t_1 - t_2)
                pass
            try:
                # print('用户id：',resp.id,'用户first_name',resp.first_name,'用户last_name',resp.last_name,'用户名 username',resp.username,'用户 phone',resp.phone)
                temp_dict = {}
                temp_dict['用户_id：'] = str(ip.id)
                temp_dict['用户_first_name'] = ip.first_name
                temp_dict['用户_last_name'] = ip.last_name
                temp_dict['用户名_username'] = ip.username
                temp_dict['用户_phone'] = str(ip.phone)
                result.append(temp_dict)
                # print('part------------->', ip.id)
            except Exception as e:
                print('part < 1W',e.args)
                continue
            #responses.append(ip)
        #responses =client.iter_participants(channel)  # 获取群组所有用户信息
    else:
        time_list_part_w.append(time.time())
        time_list_part_w.append(time.time())
        async for ip in client.iter_participants(channel,aggressive=True):
            part_num += 1
            if part_num % 100 == 0:
                time_list_part_w.append(time.time())
                print('获取了【{}】个用户'.format(part_num),'channel_id',channel_id)
            t_1 = time_list_part_w[len(time_list_part_w) - 1]
            t_2 = time_list_part_w[len(time_list_part_w) - 2]
            if (t_1 != t_2) & ((t_1 - t_2) > 15):
                # if (time_list[len(time_list) - 1] - time_list[len(time_list) - 2]) > 300:
                print('网络耗时：', t_1 - t_2)
                pass
            try:
                # print('用户id：',resp.id,'用户first_name',resp.first_name,'用户last_name',resp.last_name,'用户名 username',resp.username,'用户 phone',resp.phone)
                temp_dict = {}
                temp_dict['用户_id：'] = str(ip.id)
                temp_dict['用户_first_name'] = ip.first_name
                temp_dict['用户_last_name'] = ip.last_name
                temp_dict['用户名_username'] = ip.username
                temp_dict['用户_phone'] = str(ip.phone)
                result.append(temp_dict)
                # print('part------------->', ip.id)
            except Exception as e:
                print('part > 1W',e.args)
                continue
            # responses.append(ip)
        #responses = client.iter_participants(channel,aggressive=True)
    # async for resp in responses:
    #     try:
    #         # print('用户id：',resp.id,'用户first_name',resp.first_name,'用户last_name',resp.last_name,'用户名 username',resp.username,'用户 phone',resp.phone)
    #         temp_dict = {}
    #         temp_dict['用户_id：'] = str(resp.id)
    #         temp_dict['用户_first_name'] = resp.first_name
    #         temp_dict['用户_last_name'] = resp.last_name
    #         temp_dict['用户名_username'] = resp.username
    #         temp_dict['用户_phone'] = str(resp.phone)
    #         result.append(temp_dict)
    #         print('part------------->',resp.id)
    #         part_num += 1
    #     except Exception as e:
    #         print(e.args)
    #         pass
    print('==== 获取群成员结束，总共{}个群成员 ===='.format(part_num))
    try:
        with open('{file_local}'.format(file_local=part_file_local), 'w', encoding='utf-8') as f:
            json.dump(result_admin, f, ensure_ascii=False, indent=2)
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e.args)
        pass
# with client:
#     client.loop.run_until_complete(main())