import requests

#url = 'https://127.0.0.1/tempurl/?aid=enkac&uid=enkac'

url = 'https://127.0.0.1/renewtempauth/'
myobj = {
    'username': 'admin',
    'password': 'admin'
    }

x = requests.post(url, data=myobj, verify=False)

print(x.text)