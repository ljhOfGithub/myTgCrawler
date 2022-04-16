# import requests
import eventlet
import time

eventlet.monkey_patch()

time_limit = 100 # set timeout time 3s
init = 0

time_list = []
with eventlet.Timeout(time_limit, False):
    lst_per_hund_time = 0
    for i in range(1,11000000000000000):
        init += 1
        time.sleep(0.01)
        per_hund_time = time.time()
        if init % 10 == 0 :
            time_list.append(time.time())
            if init == 20 :
                time.sleep(2)
            print('per_hund_time',per_hund_time)

        try:
            print('lst_per_hund_time', time_list[len(time_list) - 2])
            if (per_hund_time - time_list[len(time_list) - 2]) > 2.2:
                print(per_hund_time, time_list[len(time_list) - 2])
                print('差额:', per_hund_time - time_list[len(time_list) - 2])
                break
        except :
            continue

print('over')