import requests
headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

resp = requests.get("http://10.31.161.59:8888",headers=headers)

# 获得响应中的头信息
print(resp.headers)

# 获得请求的头信息
print(resp.request.headers)

# 获得响应的内容
print(resp.text)  # 字符串格式
print(resp.content) # bytes格式
print(resp.raw)   # 原始响应内容
print(resp.json())  # json格式

