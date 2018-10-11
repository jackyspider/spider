import requests

r = requests.get("http://www.baidu.com/s",params={'wd':'hello'})
r = requests.get("http://www.baidu.com/s",params=dict(wd='python'))
