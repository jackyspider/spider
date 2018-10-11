import requests


url = ''
files = {
    'file':open('somefile.txt','rb')
}

r = requests.post(url,files=files)