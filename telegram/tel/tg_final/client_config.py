

from telethon import TelegramClient
#
# #=======================================================================
# +12345678911
api_id =10754897
api_hash = 'e42a8b8fa4fc81078852b8ed3a14feb1'
client1 = TelegramClient('tg.session', api_id, api_hash)
# client1.start(password='Wfl123456.')
client1.start()
# #===============================================================

#客户列表。需要手动添加
client_list = []
client_list.append(client1)
