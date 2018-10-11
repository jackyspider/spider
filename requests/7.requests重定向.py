import  requests

r = requests.get('http://www.baidu.com/',allow_redirects=False) # 禁用重定向
r = requests.get('http://10.31.161.59:8888/admin',allow_redirects=False)  # 允许重定向

print(r.text)