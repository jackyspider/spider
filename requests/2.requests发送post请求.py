"""
发送post请求,字典会在请求时自动转化为表单
"""

import requests
url = 'http://10.31.161.59:8888/user/register/'
r = requests.post(url,data=dict(username='python1803',password='123456'))
print(r.content)