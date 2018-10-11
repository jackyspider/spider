from requests import Request,Session

session = Session()
url = 'http://www.baidu.com'

# 构建一个请求对象
req = Request('GET',url,headers=None)

# 获得带有状态的预请求对象
request = session.prepare_request(req)
print(type(request))


# 发送请求
with session.send(request,timeout=0.5) as response:
    print(response.status_code)