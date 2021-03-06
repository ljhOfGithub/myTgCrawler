import traceback
from ast import literal_eval
import pandas as pd
import re
filenum = 4
myversion = '3'
def getUsername():
    usernameList = []
    for i in range(1,5):
        try:
            filename = 'addgroup' + str(i) + '.txt'
            with open(filename,'r',encoding='utf-8') as f:
                linkList = literal_eval(f.read())
            for link in linkList:
                try:
                    if link.startswith('https://telegramchannels.me/bots'):
                        continue
                    elif link.startswith('https://telegramchannels.me/groups'):
                        username = link[35:]
                        usernameList.append(username)
                    elif link.startswith('https://telegramchannels.me/channels'):
                        username = link[37:]
                        usernameList.append(username)
                except:
                    traceback.print_exc()
                    pass
        except:
            print(i)
    with open('username.txt','w') as f:
        print(usernameList,file=f)
def getUsername2():
    df = pd.read_csv('tglinkAll.csv')
    usernameList = []
    for index,row in df.iterrows():
        tgRe = r"(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?"
        mylist = re.findall(tgRe,row['link'])
        username = mylist[0][3]
        usernameList.append(username)
        print(username)
    with open('username2.txt','w') as f:
        print(usernameList,file=f)
        # print(len(usernameList))
# username = "BitShibaToken"
# username = 'octafx_trade_bitcoin_signal'#不需要加群也能搜索信息
min_id = 0  # 开启的消息id
limit = 100000  # 检索的消息数量
from telethon import TelegramClient
import traceback
import logging
import pandas as pd
api_id =9063315
api_hash = '39ee1e156d8f3a1f99a3c4096ef09452'
api_id =10754897
api_hash = 'e42a8b8fa4fc81078852b8ed3a14feb1'
# client_list = []
# client_list.append(client)
logname = 'search' + myversion + '.log'
logging.basicConfig(level=logging.ERROR,#控制台打印的日志级别
                    filename=logname,
                    filemode='w',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    )
import csv
async def msg(client,username):
    # search = 'address'
    search = '0x'
    messages = client.iter_messages(username, min_id=min_id, reverse=True, limit=limit, search=search)
    filename = '/home/mytg/mycsv' + myversion + '/' + username + '.csv'
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date','message','user_first','user_last'])
        try:
            async for M in messages:
                user = await client.get_entity(M.from_id)
                writer.writerow([M.date, str(M.message), user.first_name, user.last_name])
        except:
            # traceback.print_exc()
            logging.error(str(traceback.format_exc()))
def detect():
    with open('addr.txt','r') as f:
        addrlist = literal_eval(f.read())
    usernameFile = 'username' + myversion + '.txt'
    detectFile = 'detect' + myversion + '.csv'
    with open(usernameFile, 'r') as f:
        usernameList = literal_eval(f.read())
    with open(detectFile,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['group','date','message','user_first','user_last'])
        for username in usernameList:
            filename = '/home/mytg/mycsv' + myversion + '/' + username + '.csv'
            df = pd.read_csv(filename)
            for index,row in df.iterrows():
                tag = any([addr in str(row['message']).lower() for addr in addrlist])#有任何一个地址则输出
                if tag:
                    print(1)
                    writer.writerow([username,row['date'],row['message'],row['user_first'],row['user_last']])
import asyncio
async def verifyScam(client,username):
    # usernameFile = 'username' + myversion + '.txt'
    # detectFile = 'detect' + myversion + '.csv'
    # entity = await client.get_entity(username)
    # print(type(entity))
    # for att in dir(entity):
    #     print(att, getattr(entity, att))
    # username = 'digitalgoldcoin'
    try:
        entity = await client.get_entity(username)  # 如果不使用await，get_entity会返回<class 'coroutine'>
        scam = entity.scam
        if scam == True:
            print(username)
    except:
        print('error')
        print(username)
    await asyncio.sleep(1)
if __name__ == '__main__':
    client = TelegramClient('search.session', api_id, api_hash)
    client.start()
    usernameFile = 'username' + myversion + '.txt'
    with open(usernameFile, 'r') as f:
        usernameList = literal_eval(f.read())
    indexSkip = -1
    count = 0
    usernameList = usernameList[count:]
    for username in usernameList:
        # myindex = usernameList.index(username)
        if count == indexSkip:
            continue
        print(count)
        count += 1
        # print(myindex)
        # print(username)
        # client.loop.run_until_complete(msg(client,username))
        client.loop.run_until_complete(verifyScam(client,username))
# detect()
    # getUsername()
    # getUsername2()
#     for c in client_list:
#         with c:
#             # c.loop.run_until_complete(msg(c))
#             await msg(c)
    # pass
    # chat = client.get_input_entity(username)
    # chat = client.get_entity(username)
    # result = client(SearchRequest(
    #     peer=chat,      # On which chat/conversation
    #     q='query',      # What to search for
    #     filter=filter,  # Filter to use (maybe filter for media)
    #     min_date=None,  # Minimum date
    #     max_date=None,  # Maximum date
    #     offset_id=0,    # ID of the message to use as offset
    #     add_offset=0,   # Additional offset
    #     limit=1000,       # How many results
    #     max_id=0,       # Maximum message ID
    #     min_id=0,       # Minimum message ID
    #     from_id=None,    # Who must have sent the message (peer)
    #     hash=0
    # ))
    # async for message in client.iter_messages(chat, reverse=True):
    #     print(message.id, message.text)
        # print(result.stringify())
# for message in client.iter_messages(chat,filter=result):
#     print(message.message)
