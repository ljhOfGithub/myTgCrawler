# 使用api的方式查询聊天记录
import csv
username = "BitShibaToken"
min_id = 0  # 开启的消息id
limit = 100000  # 检索的消息数量
from telethon import TelegramClient, utils, errors
from telethon.sessions import StringSession
import logging
import asyncio
import traceback
from tqdm import trange
import tqdm
api_id =10754897
api_hash = 'e42a8b8fa4fc81078852b8ed3a14feb1'
PROXY_TYPE_HTTP = HTTP = 3
proxy = (3,'127.0.0.1','1080')
import time


logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
client = TelegramClient('tg.session', api_id, api_hash)
# client = TelegramClient('tg.session', api_id, api_hash,proxy=proxy)
async def tg_msg(client):
    messages = client.iter_messages(username, min_id=min_id, reverse=True, limit=limit)
    count = 0
    csvname = username + '.csv'
    with open(csvname,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date','message','user_first','user_last'])
        async for M in messages:
            # print(message)
            # writer.writerow([message['date'],message['message'],message['from_id']])
            try:
                user = await client.get_entity(M.from_id)
                # print(user)
                # print(M.message)
                writer.writerow([M.date, str(M.message), user.first_name, user.last_name])
            except:
                # traceback.print_exc()
                logging.debug(M)
                logging.debug(str(traceback.format_exc()))
            count += 1
            print(count)
    # print(messages)
# 进行消息处理
# async for message in messages:
#     print(message)
client_list = []
client_list.append(client)
for c in client_list:
    with c:
        # t = tqdm.tqdm(total=limit, desc='下载进度')
        c.loop.run_until_complete(tg_msg(c))
        # t.close()
#搜索到的很多group的信息都是无用信息，不如直接用信息搜索功能搜索地址信息再手动筛选