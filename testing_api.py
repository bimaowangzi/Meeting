# Name: testing_api.py
# Description: Simple testing suite for the API.

import requests

from requests.auth import HTTPBasicAuth

r = requests.get("http://localhost:5000/")
print(r.text)
r = requests.get("http://localhost:5000/meeting", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.get("http://localhost:5000/person")
print(r.text)
r = requests.get("http://localhost:5000/person", auth = HTTPBasicAuth('admin','password'))
print(r.text)
# do note that the post/put probably requires a json.
# in that case, create a payload = {'key1': 'value1' ...}
# then: requests.put(<url>, params = payload)
# see more at http://www.python-requests.org/en/latest/user/quickstart/

r = requests.put("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.post("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.get("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.delete("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.put("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.post("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.get("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.delete("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)