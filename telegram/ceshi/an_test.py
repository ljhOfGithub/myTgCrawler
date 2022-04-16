import requests
import json
url = "https://api.duanshu.com/h5/content/detail/39cfe042780d4167b6ffa3a280707a30?shop_id=13g064j7d524gd6285"

payload = {}
headers = {
   'Accept': 'application/json',
   'Origin': 'https://lbjgg.duanshu.com',
   'Referer': 'https://lbjgg.duanshu.com/',
   'Sec-Fetch-Mode': 'cors',
   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML',
   'x-member': '%7B%22id%22:%2230efca3916b54eb49724320e56392d3e%22',
   'x-platform': 'h5',
   'x-shop': '13g064j7d524gd6285'
}

response = requests.request("GET", url, headers=headers, data = payload)
print(json.loads(response.text.encode('utf8')))
