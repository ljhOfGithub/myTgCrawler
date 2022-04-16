#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/9/12 9:57
# @Author: weifulong
# @File  : config.py
# coding=utf-8
import datetime
import json
import os
import re
import traceback
import threading
import tg_get_userinfo_by_id_final
import tg_msg_final
import tg_get_group_info_final
import tg_group_part_info_final
from telegram.tel.tg_final import client_config


##################  手动更改区域  #############################################################

# =============== 群组信息存放位置，需要先确定群组信息存放位置=======     ##
# 文件储存路径为 例如： db\电报账户\tg组ID\msg.json
root_floder = 'D:\\\\db\\\\'

# 获取聊天信息日期
msg_date = datetime.date(2019, 7, 1)

#从第client_id个账号开始获取,0为第一个账号
client_id = 0
#从第gp_id个群开始获取，0为第一个群。
#到第gp_id_end个群结束。 如果数值为 0 则默认为该账号下总群组的个数。
gp_id = 0
gp_id_end = 0
# 控制开关 ，是否进行相应的函数调用  1：使 用 0：不使用
# !!!!群的信息，必须要获取一次之后才可以关闭， 否则群信息，群成员均无法获得！！！
button_group = 1  # 获取群的信息  1：使 用 0：不使用
button_part = 1  # 获取群成员  1：使 用 0：不使用
button_msg = 1  # 获取群聊天信息总开关
get_channel = 1  # 0:默认获取群、频道内容  1：只获取群内容
download_media = 0  # 下载媒体文件  1：使 用 0：不使用
download_normal = 0  # 下载文本内容信息  1：使 用 0：不使用
button_getUserInfo_byId = 0  # 获取成员信息通过 聊天信息的 id  速度：300分/10000 id


############################################################################################


# 文件输出位置 创建对应的文件夹,以及文件
# floder_name :文件夹名称
# account_floder : 账户
# file_type：msg、 msg_user、 part、group

# 获取聊天信息数量（目前已经停用）
msg_num = 100000
msg_id = 142280

def mkdir(account_floder, floder_name, file_type):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    floder_name = re.sub(rstr, "_", floder_name)  # 替换为下划线
    path = root_floder + account_floder + "\\\\" + floder_name
    file_need_make = path + '\\\\' + '{}.json'.format(file_type)
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path):
        with open(file_need_make, 'w', encoding='utf-8') as ff:
            print(file_need_make, '创建成功')
    return file_need_make


# acount_floder_name  :用账户名 创建文件夹
# floder_name : 用组名称，创建文件夹
# group_id : 组id，用于获取聊天信息
def mkFIle_localtion(acount_floder_name, floder_name, group_id, group_name, group_num):
    file_local_list = []
    # 创建文件夹
    rstr = r"[\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    count_floder_title = re.sub(rstr, "_", acount_floder_name)  # 替换为下划线
    group_floder_title = re.sub(rstr, "_", floder_name)  # 替换为下划线
    msg_json = ' '
    # msg_user msg_user 文件的位置
    msg_user_json = ' '
    # part part 文件的位置
    part_json = ' '
    file_msg_location = msg_json
    file_part_location = part_json
    file_msg_user_location = msg_user_json
    file_part_admin_location = ' '
    file_local_list.append(file_msg_location)  # msg文件位置
    file_local_list.append(file_part_location)  # part文件位置
    file_local_list.append(file_part_admin_location)  # part文件位置
    file_local_list.append(group_id)  # 组id
    file_local_list.append(group_name)  # 组名
    file_local_list.append(group_num)  # 组成员人数
    file_local_list.append(file_msg_user_location)  # msg 中人员信息文件

    # print("\n---》mkFIle_localtion《---\n")
    return file_local_list


# ============  主程序运行   ================
def run(clientList):
    for clitn_i in range(client_id,len(clientList)):
        client = clientList[clitn_i]
        print('用户 ---》', client.get_me().phone)
        with client:
            username = str(client.get_me().phone)
            # 用于储存所有 文件夹名称 同时列表也存在 文件名称 群成员.json 群信息.json
            file_total_list = []
            # 获取 group信息 文件路径
            group_file_path = mkdir(username, 'group_info', 'group_info')
            # 获取群组信息，并存放在指定位置
            if int(button_group) == 1:
                # group/channel 信息文件 位置
                print('用户 ---》', username, ' 获取群信息')
                try:
                    client.loop.run_until_complete(tg_get_group_info_final.tg_get_group_info(client, group_file_path))
                except Exception as e:
                    print('tg_get_group_info', e.args)
                    pass
                print('！！！群信息写入结束！！！')
            # 通过获取的群组信息，进行内容，群成员获取
            try:
                with open('{}'.format(group_file_path), 'r', encoding='utf-8') as f:
                    result = json.loads(f.read())
                    # print(result[0]['频道channel名：'])
                    for i in range(0, len(result)):
                        try:
                            if get_channel == 0:
                                if (str(result[i]).find('聊天组Group名：')) > 0:
                                    f_name = client.get_me().first_name if client.get_me().first_name else ''
                                    l_name = client.get_me().last_name if client.get_me().last_name else ''
                                    count = f_name + l_name
                                    local = mkFIle_localtion(count, result[i]['聊天组Group名：'], result[i]['组id：'],
                                                             result[i]['聊天组Group名：'], result[i]['群组总人数：'])
                                    file_total_list.append(local)
                                else:
                                    # "此处，如果是需要channel 的话，可以吧pass注释，下面的代码激活"
                                    # pass
                                    count = client.get_me().first_name + client.get_me().last_name
                                    # print('频道channel名：',result[i]['频道channel名：'],result[i]['频道id：'])
                                    local = mkFIle_localtion(count,result[i]['频道channel名：'], result[i]['频道id：'],
                                                             result[i]['频道channel名：'], result[i]['频道总人数：'])
                                    file_total_list.append(local)
                            else:
                                if (str(result[i]).find('聊天组Group名：')) > 0:
                                    f_name = client.get_me().first_name if client.get_me().first_name else ''
                                    l_name = client.get_me().last_name if client.get_me().last_name else ''
                                    count = f_name + l_name
                                    local = mkFIle_localtion(count, result[i]['聊天组Group名：'], result[i]['组id：'],
                                                             result[i]['聊天组Group名：'], result[i]['群组总人数：'])
                                    file_total_list.append(local)
                                else:
                                    pass
                        except Exception as e:
                            print('将内容合并：', e.args, result[i])
                            print(traceback.format_exc())
                            pass
            except Exception as e:
                print('获取的群组信息：', e.args)
                pass

            # 获取 群、频道 聊天信息内容，群成员
            # file_total_list[i][0]：空（msg文件位置）
            # file_total_list[i][1]：空（part文件位置）
            # file_total_list[i][2]：空
            # file_total_list[i][3]：group/channel id
            # file_total_list[i][4]：group/channel name
            # file_total_list[i][5]：group/channel 总人数
            # file_total_list[i][6]：空 （msg 中人员信息文件）



            #从指定账号的指定组，下一个账号则从第一个群组开始跑
            if clitn_i == client_id & gp_id < len(file_total_list):
                gp_id1 = gp_id
                print('第{}个群开始'.format(gp_id1))
            else:
                gp_id1 = 0
                print('第{}个群开始'.format(gp_id1))

            # 控制组区间
            if gp_id_end != 0 & gp_id_end < len(file_total_list):
                gp_id_end1 = gp_id_end
                print('到{}个群结束'.format(gp_id_end1))
            else:
                gp_id_end1 = len(file_total_list)
                print('到{}个群结束'.format(gp_id_end1))

            for i in range(gp_id1, gp_id_end1):
                # 获取 群成员信息
                if int(button_part) == 1:
                    # part 信息文件 位置
                    group_part_path = mkdir(username, file_total_list[i][3], 'part')

                    print('用户 ---》', username, " 获取群成员")
                    try:
                        print('群组---》', file_total_list[i][4])
                        client.loop.run_until_complete(
                            tg_group_part_info_final.tg_get_group_part(client, group_part_path, file_total_list[i][2],
                                                                       file_total_list[i][3], file_total_list[i][5]))
                    except Exception as e:
                        print("tg_get_group_part", e.args)
                        pass
                    print('！！！群成员写入结束！！！')
                # 获取群聊天信息
                if int(button_msg) == 1:
                    # msg 信息文件 位置
                    group_msg_path = mkdir(username, file_total_list[i][3], 'msg')
                    #纯 媒体文件 下载路径
                    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                    floder_name = re.sub(rstr, "_", file_total_list[i][3])  # 替换为下划线
                    group_media_path = root_floder + username + "\\\\" + floder_name + "\\\\"
                    print('用户---》', username, " 获取聊天信息")
                    try:
                        print('群组---》', file_total_list[i][4])
                        # print(file_total_list[i][1],file_total_list[i][2])
                        client.loop.run_until_complete(
                            tg_msg_final.tg_msg(client, msg_num, group_msg_path, file_total_list[i][3], msg_date,msg_id,
                                                group_media_path,download_media,download_normal))
                    except Exception as e:
                        print("tg_msg", e.args)
                        pass
                    print('！！！聊天信息写入结束！！！')
                # 通过群消息获取用户 信息
                if int(button_getUserInfo_byId) == 1:
                    # msg_user msg_user 文件的位置
                    group_msg_path = mkdir(username, file_total_list[i][3], 'msg')
                    group_msg_user_path = mkdir(username, file_total_list[i][3], 'msg_user')
                    print('用户 ---》', username, " 获取聊天信息群成员")
                    try:
                        print('群组---》', file_total_list[i][4])
                        client.loop.run_until_complete(
                            tg_get_userinfo_by_id_final.getUserInfo_byId(client, group_msg_path, group_msg_user_path))
                    except Exception as e:
                        print("tg_msg_user", e.args)
                        pass
                    print('！！！聊天信息群成员更新结束！！！')


run(client_config.client_list)
