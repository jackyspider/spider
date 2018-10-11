import requests
url = "http://pic171.nipic.com/file/20180705/5053868_230805401034_2.jpg"
r = requests.get(url)
with open('demo.jpg','wb') as f:
    f.write(r.content)
