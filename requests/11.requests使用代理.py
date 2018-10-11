import requests

proxies = {
    'http':'http://101.236.35.98:8866',
    'https':'https://180.121.132.184:808'
}


r = requests.get('http://www.ip138.com/',proxies=proxies)
print(r.text)