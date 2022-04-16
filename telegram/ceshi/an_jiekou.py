import requests,json
import re,time,os

url = "https://api.duanshu.com/h5/content/lists?count=1000&page=1&shop_id=13g064j7d524gd6285"
# url_article = "https://api.duanshu.com/h5/content/detail/39cfe042780d4167b6ffa3a280707a30?shop_id=13g064j7d524gd6285"
payload = {}
headers = {
   'Accept': 'application/json, text/plain, */*',
   'Origin': 'https://lbjgg.duanshu.com',
   'Referer': 'https://lbjgg.duanshu.com/',
   'Sec-Fetch-Mode': 'cors',
   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
   'x-member': '%7B%22id%22:%2230efca3916b54eb49724320e56392d3e%22,%22timestamp%22:1611819703,%22randomstr%22:%22ayy4dfeWycr1%22,%22expire%22:1612424503,%22signature%22:%2265d50c67a6baa17ba8719ab6e3c511d14e0d186f%22%7D',
   'x-platform': 'h5',
   'x-shop': '13g064j7d524gd6285'
}
#请求网页链接标题
total_artical = []  #
total_title = []  # 文章头
total_url = []  # 文章链接
total_final = []  # 存储最终结果
path='/Users/weifulong/Desktop/bi/'


def list():
    try:
        response = requests.request("GET", url, headers=headers, data = payload)
        #网页链接标题详细内容,及总页数
        req_json1 = json.loads(response.text)['response']['data']
        return req_json1
    except Exception as e:
        print('list失败')
        pass
    #文章内容
def art():
#获取文章列表
    req_json = list()
    print('列表获取成功！！！')
    for i in range(0,len(req_json)):
        # 请求文章具体内容。# 最终结果，文章url   1
        url_article ='https://api.duanshu.com/h5/content/detail/'+req_json[i]['hashid'] +'?shop_id=13g064j7d524gd6285'
        print('url获取成功')
        #文章是否收费
        price_article = req_json[i]['price']
        #文章时间
        time_article = req_json[i]['up_time']
        # 文章详细内容
        try:
            # 文章请求
            response_art = requests.request("GET", url_article, headers=headers)
            time.sleep(5)
            print(url_article + '状态：' + str(response_art.status_code))
            req_art = json.loads(response_art.text.encode('utf-8'))['response']['data']
            # 最终结果，文章标题  0
            req_art_title = req_art['title']
            # 最终结果，文章内容   4
            req_art_content = req_art['content'].replace('&nbsp;', '')#去除html文件
            req_art_content_final = re.sub('<[^<]+?>', '', req_art_content).replace('\n', '').strip()
            #文章写入
            file_write(req_art_title,url_article,price_article,time_article,req_art_content_final)
            # 结果存储每一篇文章
        except Exception as e:
            print(e.args)
def file_write(req_art_title,url_article,price_article,time_article,req_art_content_final):
    #文件名称
    file_name = time_article+'-'+price_article +'-'+req_art_title
    #文件内容
    file_content =file_name + '\n'+ url_article + '\n' + req_art_content_final
    with open(path+file_name+'.txt','w') as f:
        f.write(file_content)
    print(file_name,'写入成功')

def change_file():
    file_list = os.listdir(path)
    for i in file_list:
        file_name = i.replace('.txt','.word')
        os.rename(path+i,path+file_name)

#所有文章，写入同一个文件
def file_toall():
    result1 = ''
    file_list = os.listdir(path)
    file_list.remove('.DS_Store')
    file_list.sort()
    for i in file_list:
        file_name_1 = path+i
        # print(file_name_1)
        with open(file_name_1,'r') as f :
            result = f.read()+'\n\n\n'+'====================================='+'\n\n\n'
            print("读取成功")
        result1 = result1+result

    with open(path+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )+'-汇总.txt','w') as f1:
        print("写入成功")
        f1.write(str(result1))

if __name__ == '__main__':
    # art()
    file_toall()