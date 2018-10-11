import requests

url = 'http://www.baidu.com'
try:

    r = requests.get(url=url,timeout=1)
except Exception as e:
    print("{url}请求超时.".format(url=url))

print(type(r.request))