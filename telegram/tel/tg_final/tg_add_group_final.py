#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/9/14 16:48
# @Author: weifulong
# @File  : add_group.py


import re
import asyncio
import time
from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telegram.tel.tg_final import client_config

####################### 手动修改区域 ##########################################################
# 未加群的文件
import time
#输入需要加群的文件地址
file_local = 'C:\\Users\\DELL\\Desktop\\qunxinxi.txt'
#输入需要导出未加群成功的群地址的文件地址
file_local_out = 'C:\\Users\\DELL\\Desktop\\qunxinxi_error.txt'
##############################################################################################


# ===============全局变量区域===============
group_temp_result = []  # 临时储存结果
group_final_joinchat_result = []  # 加入到joinchat 邀请群
group_final_result = []  # 加入到公开的群
# 客户列表。需要手动添加
client_list_group = []

for i in client_config.client_list:
    client_list_group.append(i)
total_account = len(client_config.client_list)


# ================================================

error_group_list =[]

# 获得群组链接，把群组链接区分，加入到对应的列表中
def get_group_list():
    print("123456")
    global group_final_joinchat_result
    global group_final_result
    with open('{file_local}'.format(file_local=file_local), 'r', encoding='utf-8') as file:
        for f in file.readlines():
            group_temp_result.append(f)
    for resu in group_temp_result:
        patr = re.split(r'/', resu)
        if len(patr) == 3:  # 私人链接
            group_final_joinchat_result.append(patr[2].replace('\n', ''))
        if len(patr) == 2:  # 公开链接
            group_final_result.append(str(resu).replace('\n', ''))


# 第几个用户开始添加
async def main(client_i, start_group, end_group, start_group_joinChat, end_group_joinChat, total_num_group,
               total_num_join_chat):
    print("用户{}开始：==========".format(client_i + 1),'公开群组，从{}开始'.format(start_group),'到{}结束'.format(end_group),'私有群组从{}'.format(start_group_joinChat),'到{}'.format(end_group_joinChat))
    print('总公开群组',total_num_group,'总私有群组',total_num_join_chat)
    # joinchat_step = int(len(group_final_joinchat_result)/total_account)
    # step = int(len(group_final_result)/total_account)
    # print('每个用户添加的私人群组：',joinchat_step,'每个用户添加的公开群组：',step)
    count_num = 0
    # ================自动添加公开群组====================
    # total_num : 总共多少个群组，用于结束判断
    if end_group <= total_num_group:
        for i in range(start_group, end_group):
            time.sleep(20)  # 每隔20秒加群
            # print('第 {group_id} 个公开链接 {link} ---> '.format(group_id=i + step * int(client_i),link = group_final_result[i + step * int(client_i)]))

            try:
                print('第 {group_id} 个公开链接 {link} ---> '.format(group_id=i, link=group_final_result[i - 1]))
                await client_list_group[client_i](JoinChannelRequest('https://{}'.format(group_final_result[i - 1])))
                print("【用户{}】 加群成功：--->".format(client_i + 1))
                count_num += 1
            except Exception as e:
                print("【用户{}】 加群失败：--->".format(client_i + 1))
                error_group_list.append('https://{}'.format(group_final_result[i - 1]))
                continue
                # print(e.args[0])
        print("【用户{}】 加群数量统计：============》{count_num}".format(client_i + 1, count_num=count_num))
    count_num_join = 0
    if end_group_joinChat <= total_num_join_chat:
        for j in range(start_group_joinChat, end_group_joinChat):
            time.sleep(30)  # 每隔60秒加群

            try:
                print('第 {group_id} 个私人链接 {link}---> '.format(group_id=j, link=group_final_joinchat_result[j - 1]))
                # time.sleep(20)
                # updates1 = await client_list_group[client_i](ImportChatInviteRequest('{}'.format(group_final_joinchat_result[j - 1])))
                updates1 =await client_list_group[client_i](functions.messages.ImportChatInviteRequest(hash='{}'.format(group_final_joinchat_result[j - 1]) ))
                #print('updates1',updates1)
                print("【用户{}】私人链接加入成功：--->".format(client_i + 1) + str(group_final_joinchat_result[j - 1]))
                count_num_join += 1
                # if (count_num_join % 5 == 0):
                #     time.sleep(1400)
            except Exception as e:
                print("【用户{}】私人链接加入失败：--->".format(client_i + 1) + str(group_final_joinchat_result[j - 1]))
                print(e.args)
                error_group_list.append('t.me/joinchat/'+str(format(client_i + 1)))
                continue
        print("【用户{}】 加群数量统计：============》{count_num_join}".format(client_i + 1, count_num_join=count_num_join))


# 先对总群组进行划分

# for j in range(0,len())
if __name__ == '__main__':
    # client_list_group = ['A', 'B', 'C']
    get_group_list()
    gfr = len(group_final_result)
    gfjr = len(group_final_joinchat_result)
    print('总共组：', gfr, '总共私有组', gfjr)

    if int(gfr / 20) + 1 < int(gfjr / 5) + 1:
        count_to_run = int(gfjr / 5) + 1
    else:
        count_to_run = int(gfr / 20) + 1
    # 每个用户需要循环次数
    for i in range(0, int(count_to_run / len(client_list_group))+1):
        print("每个用户需要添加的轮回次数：{}".format(int(count_to_run / len(client_list_group))+1))
        # 第几个用户开始
        for j in range(0, len(client_list_group)):
            # 判定每个用户每次加多少群组
            start_group = j * 20 + 20 * len(client_list_group) * i
            end_group = start_group + 20
            start_group_joinChat = j * 5 + 5 * len(client_list_group) * i
            end_group_joinChat = start_group_joinChat + 5
            # print(start_group,end_group,start_group_joinChat,end_group_joinChat)
            print('用户添加公开群组从：', start_group, '到', end_group, ' 私有群组从', start_group_joinChat, '到', end_group_joinChat)
            # 用户开始
            with client_list_group[j]:
                client_list_group[j].loop.run_until_complete(
                    main(j, start_group, end_group, start_group_joinChat, end_group_joinChat, gfr, gfjr))
            # print(client_list_group[i])
            # 用户切换 需要休息 120s
            print('=======用户切换 需要休息 120s===========')
            time.sleep(120)
    with open(file_local_out,'w') as f:
        for error in error_group_list:
            f.write(error+'\n======\n')
