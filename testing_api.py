# Name: testing_api.py
# Description: Simple testing suite for the API.

import requests

r = requests.get("http://localhost:5000/")
print(r.text)
r = requests.get("http://localhost:5000/meeting")
print(r.text)
r = requests.get("http://localhost:5000/person")
print(r.text)

# do note that the post/put probably requires a json.
# in that case, create a payload = {'key1': 'value1' ...}
# then: requests.put(<url>, params = payload)
# see more at http://www.python-requests.org/en/latest/user/quickstart/

r = requests.put("http://localhost:5000/meeting/1337")
print(r.text)
r = requests.post("http://localhost:5000/meeting/1337")
print(r.text)
r = requests.get("http://localhost:5000/meeting/1337")
print(r.text)
r = requests.delete("http://localhost:5000/meeting/1337")
print(r.text)
r = requests.put("http://localhost:5000/person/1337")
print(r.text)
r = requests.post("http://localhost:5000/person/1337")
print(r.text)
r = requests.get("http://localhost:5000/person/1337")
print(r.text)
r = requests.delete("http://localhost:5000/person/1337")
print(r.text)