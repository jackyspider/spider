import requests

# 创建一个会话对象
session = requests.Session()

# 地址级别的参数可以垮请求保持
session.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = session.get('http://httpbin.org/cookies')
print(r.text)

# 函数级别的参数不会被跨请求保持
resp = session.get('http://httpbin.org/cookies',cookies={'name':'xiaoming'})
print(resp.text)

resp = session.get('http://httpbin.org/cookies')
print(resp.text)


# 会话可以用来提供默认数据
session = requests.Session()
session.auth = ('gavinsun','123456')
session.headers.update({'x-test': 'true'})
# both 'x-test' and 'x-test2' are sent
r = session.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
print(r.request.headers)


# 在 with 前后文管理器中使用session,确保session自动关闭
with requests.Session as session:
    session.get('http://www.baidu.com')