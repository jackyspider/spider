import json
import requests

url = ""
user = {
    'username':"gavin"
}
requests.post(url,data=json.dumps(user))
requests.post(url,json=user)
