import traceback
from ast import literal_eval
filenum = 4
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
# username = "BitShibaToken"
# username = 'octafx_trade_bitcoin_signal'#不需要加群也能搜索信息
min_id = 0  # 开启的消息id
limit = 100000  # 检索的消息数量
from telethon import TelegramClient
import traceback
api_id =9063315
api_hash = '39ee1e156d8f3a1f99a3c4096ef09452'
# client_list = []
# client_list.append(client)
async def msg(client,username):
    search = 'address'
    messages = client.iter_messages(username, min_id=min_id, reverse=True, limit=limit, search=search)
    print(messages)
    try:
        async for M in messages:
            print(M)
    except:
        traceback.print_exc()
if __name__ == '__main__':
    client = TelegramClient('search.session', api_id, api_hash)
    client.start()
    with open('username.txt', 'r') as f:
        usernameList = literal_eval(f.read())
    for username in usernameList:
        client.loop.run_until_complete(msg(client,username))
    # getUsername()
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
# logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
#                     filename='search.log',
#                     filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
#                     #a是追加模式，默认如果不写的话，就是追加模式
#                     format=
#                     '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
#                     #日志格式
#                     )