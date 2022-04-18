#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/9/14 16:48
# @Author: weifulong
# @File  : add_group.py

#
from telethon.tl.types import PeerChannel

import client_config

####################### 手动修改区域 ##########################################################
# 未加群的文件
import time
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from ast import literal_eval
file = r'addgroup.txt'

ff_list = []

with open(file,'r',encoding='utf-8') as f:
    ff_list = literal_eval(f.read())
#
async def join_group_by_id(client):
    client_phone = await client.get_me()
    # print(client_phone.phone)
    count_success = 0
    # print('用户',client_phone.phone,'开始加群')
    channel = ''
    for ch in ff_list:
        try:
            # channel_id = ch_id
            # channel = 'STunionn'
            if ch.startswith('https://telegramchannels.me/bots'):
                # print('wrong format')
                continue
            elif ch.startswith('https://telegramchannels.me/groups'):
                channel = ch[34:]
                # channel = await client.get_entity(PeerChannel(int('{channel_id}'.format(channel_id=channel_id))))
                await client(JoinChannelRequest(channel))
                # channel_hash = ch
                # await client(ImportChatInviteRequest(hash='hlQ3QhNi6q05ZDIx'))
                print('加群成功',channel)
                # print('加群成功',channel_hash)
                count_success += 1
            elif ch.startswith('https://telegramchannels.me/channels'):
                channel = ch[36:]
                await client(JoinChannelRequest(channel))
                print('加群成功',channel)
                count_success += 1

        except Exception as e:
            print('加群失败',e.args)
            pass
    print('总共成功数量：',count_success)

for c in client_config.client_list:
    with c:
        c.loop.run_until_complete(join_group_by_id(c))
#addgroup:ethereum搜索
#addgroup2:blockchain搜索
#addgroup3:cryptocurrency搜索
#addgroup4:nft搜索