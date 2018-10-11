url = 'http://sqdownb.onlinedown.net/down/FastStoneCapture44264.zip'
import requests
filename = url.split('/')[-1]
r = requests.get(url,stream=True)
with open(filename,'wb') as f:
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
