#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/9/12 9:57
# @Author: weifulong
# @File  : test2.py
# coding=utf-8
import json
import time
import requests
import eventlet
import time

from telethon import TelegramClient
from telethon import TelegramClient, sync, events
from datetime import datetime, timedelta, timezone

from telethon.tl import functions
import eventlet
import time
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

eventlet.monkey_patch()
time_limit = 3  # set timeout time 3s


async def tg_msg(client, msg_num, file_local, channel_id, date, msg_id):
    # api_id = config.api_id
    # api_hash = config.api_hash
    client = client
    # channel = '阿雷科技'
    # All of these work and do the same.
    # lonami = client.get_entity('lonami')
    # lonami = client.get_entity('t.me/lonami')
    # lonami = client.get_entity('https://telegram.dog/lonami')
    #
    # # Other kind of entities.
    # channel = client.get_entity('telegram.me/joinchat/AAAAAEkk2WdoDrB4-Q8-gg')
    # contact = client.get_entity('+34xxxxxxxxx')
    # friend = client.get_entity(friend_id)
    #
    # # Getting entities through their ID (User, Chat or Channel)
    # entity = client.get_entity(some_id)
    #
    # # You can be more explicit about the type for said ID by wrapping
    # # it inside a Peer instance. This is recommended but not necessary.
    # from telethon.tl.types import PeerUser, PeerChat, PeerChannel
    #
    # my_user = client.get_entity(PeerUser(some_id))
    # my_chat = client.get_entity(PeerChat(some_id))

    # 内容：message
    # 日期：date
    # 发表的用户id： from_id
    # 媒体id：media.id
    # 照片id：media.photo.id
    # 文件id：media.document.id

    time_limit = 15  # set timeout time 3s,如果15s数值没有变动

    result = []

    channel_id = channel_id
    # channel_id = '1172149960'
    # 两种id 均可以
    entity = await client.get_entity(PeerChannel(int('{channel_id}'.format(channel_id=channel_id))))

    count_msg = 0
    # 存放时间戳
    time_list = []
    # print("开始时间：{}".format(start_time))
    eventlet.monkey_patch()
    try:
        # with eventlet.Timeout(10,True): #1500s限制
        time_list.append(time.time())
        # async for message in client.iter_messages(entity,limit=msg_num,offset_date=date,reverse=True,offset_id=msg_id):
        async for message in client.iter_messages(entity, wait_time=1.2, offset_date=date, reverse=True):
            # start_time = time.time()
            time_list.append(time.time())
            t_1 = time_list[len(time_list) - 1]
            t_2 = time_list[len(time_list) - 2]
            if (t_1 != t_2) & ((t_1 - t_2) > 15):
                # if (time_list[len(time_list) - 1] - time_list[len(time_list) - 2]) > 300:

                if t_1 - t_2 > 1800:
                    print('跳出，此群组')
                    break
                else:
                    print(print('网络耗时：', t_1 - t_2))
                    pass
            temp_dict = {}
            # print(message)

            try:
                message_media_id = message.media.id
            except:
                message_media_id = ' '
            try:
                message_medis_photo_id = message.medis.photo.id
                # client.download_profile_photo(str(message.medis.photo.file_reference))
                # print("下载成功")
            except:
                message_medis_photo_id = ' '
            try:
                message_media_document_id = message.media.document.id
            except:
                message_media_document_id = ' '
            try:

                temp_dict['信息内容：'] = str(message.message)
                temp_dict['发信息时间：'] = str(
                    message.date.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))))
                temp_dict['发言者ID：'] = str(message.from_id)
                temp_dict['消息ID：'] = str(message.id)
                # 获取发言者信息
                # try:
                #     result_msg = await client.get_entity(PeerUser(int("{}".format(str(message.from_id)))))
                #     temp_dict['发言者first_name：'] = str(result_msg.first_name)
                #     temp_dict['发言者last_name ：'] = str(result_msg.last_name)
                #     temp_dict['发言者username ：'] = str(result_msg.username)
                #     temp_dict['发言者phone ：'] = str(result_msg.phone)
                # except:
                #     pass
                temp_dict['媒体ID：'] = str(message_media_id)
                temp_dict['照片ID：'] = str(message_medis_photo_id)
                temp_dict['文件ID：'] = str(message_media_document_id)
                # format_str = str(temp_dict['信息内容：']).strip().replace('\n','').replace('\r','')
                result.append(temp_dict)
                # result.append('\n')
                # print(msg)
                count_msg += 1

                if count_msg % 1000 == 0:  # 每一百就开始计时
                    # per_hund_time = time.time()
                    try:
                        print("已经获取【{}】条信息".format(count_msg), "耗时：",
                              time_list[int(1000 * (count_msg / 1000))] - time_list[int(1000 * (count_msg / 1000 - 1))],
                              'channel_id', channel_id)
                        if time_list[int(1000 * (count_msg / 1000))] - time_list[
                            int(1000 * (count_msg / 1000 - 1))] > 300:
                            break
                    except Exception as e:
                        print('耗时错误{此错误无关紧要}', e.args)
                    # if t_1 != t_2:
                    #     print("耗时：",t_1-t_2)
            except Exception as e:
                print('msg_error：', e.args)
                pass

    except Exception as e:
        print('client.iter_messages 错误', e.args)
    print("===== 获取信息结束 ========")

    # print("===== 总耗时：  {} ========".format(time.time()-start_time))
    #     文件写入，格式为json
    with open('{file_local}'.format(file_local=file_local), 'w', encoding='utf-8', ) as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        # for re in result:
        # f.write(str(result))

# with client:
#     client.loop.run_until_complete(tg_msg_final())