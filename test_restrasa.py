# import urllib2
import urllib.request as urllib2
import urllib
import json
import random
import time

ip = "localhost"
# url = 'http://192.168.1.70:5005/webhooks/rest/webhook/'
url = 'http://'+ip+':5005/webhooks/rest/webhook/'
text = "hello"

data = '{"sender":"nao", "message":"' + text + '"}'
data = urllib.parse.urlencode(data).encode("utf-8")

req = urllib2.Request(url, data=data)
f = urllib2.urlopen(req)
class Response:
    pass
response = Response()
response.code = f.getcode()
response.body = f.read()
print(response.body)
r = json.loads(response.body)
if (r):
	r = r[0]['text'].encode("UTF-8")
print(r)
