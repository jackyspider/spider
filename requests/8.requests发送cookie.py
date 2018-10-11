import requests

url = 'http://10.31.161.59:8888/'
headers = {
    'User-Agent':'afasdfasfasdf',
}
cookies = dict(
    sessionid = 'swkbut2xrt2c3rhhwubamp80oa2p7tzw',
    csrftoken = 'e6JLs6n2u4gPDrd8l3XVkUhhvCldxUvXhJ0SHJGiV1oUbnTwv12CR9GTvzX6l9EC'
)
resp = requests.get(url,headers=headers,cookies=cookies)
print(resp.text)
