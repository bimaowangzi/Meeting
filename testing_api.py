# Name: testing_api.py
# Description: Simple testing suite for the API.

import requests

from requests.auth import HTTPBasicAuth

r = requests.get("http://localhost:5000/person", auth = HTTPBasicAuth('admin','password'), headers={"content-type":"text"})
print(r.text)
r = requests.get("http://localhost:5000/person", auth = HTTPBasicAuth('admin','password'), headers={"content-type":"application/json"})
print(r.text)
r = requests.get("http://localhost:5000/person", auth = HTTPBasicAuth('admin','password'))
print(r.text)

r = requests.get("http://localhost:5000/meeting", auth = HTTPBasicAuth('admin','password'), headers={"content-type":"text"})
print(r.text)
r = requests.get("http://localhost:5000/meeting", auth = HTTPBasicAuth('admin','password'), headers={"content-type":"application/json"})
print(r.text)
r = requests.get("http://localhost:5000/meeting", auth = HTTPBasicAuth('admin','password'))
print(r.text)

print("schedule Junsheng to conflict room1")
r = requests.get("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.post("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'), params = {'m_id': '4', 'p_id': '2'})
print(r.text)

print("schedule Junsheng to conflict room2")
r = requests.get("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.post("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'), params = {'m_id': '5', 'p_id': '2'})
print(r.text)

print("schedule Junsheng to conflict room3")
r = requests.get("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.post("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'), params = {'m_id': '6', 'p_id': '2'})
print(r.text)

print("schedule Junsheng to Canteen")
r = requests.get("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.post("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'), params = {'m_id': '2', 'p_id': '2'})
print(r.text)

print("unschedule Junsheng to Canteen")
r = requests.get("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'))
print(r.text)
r = requests.delete("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'), params = {'m_id': '2', 'p_id': '2'})
print(r.text)

# Person test
print("Attempt to put Hazel")
r = requests.put("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'), params = {'name': 'Hazel'})
print(r.text)
print("Attempt to post Hazel")
r = requests.post("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'), params = {'name': 'Hazel'})
print(r.text)
r = requests.get("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
print("Attempt to change person 1337 to Junqi")
r = requests.put("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'), params = {'name': 'Junqi'})
print(r.text)
r = requests.get("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
print("Attempt to delete Junqi")
r = requests.delete("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)

# Meeting test
print("Attempt to put Meeting at ISH")
r = requests.put("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'), params = {'start_time': '1300', 'end_time': '2000', 'location': "ISH"})
print(r.text)
r = requests.get("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
print("Attempt to post Meeting at ISH")
r = requests.post("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'), params = {'start_time': '1300', 'end_time': '2000', 'location': "ISH"})
print(r.text)
r = requests.get("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
print("Attempt to change meeting 1337 to Home")
r = requests.put("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'), params = {'start_time': '1300', 'end_time': '2000', 'location': "ISH"})
print(r.text)
r = requests.get("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)
print("Attempt to delete meeting at Home")
r = requests.delete("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'), params = {'start_time': '1300', 'end_time': '2000', 'location': "ISH"})
print(r.text)
print("Attempt to get deleted meeting at Home")
r = requests.get("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
print(r.text)