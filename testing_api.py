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

# r = requests.get("http://localhost:5000/")
# print(r.text)
# r = requests.get("http://localhost:5000/meeting", auth = HTTPBasicAuth('admin','password'))
# print(r.text)
# r = requests.get("http://localhost:5000/person")
# print(r.text)
# r = requests.get("http://localhost:5000/person", auth = HTTPBasicAuth('admin','password'))
# print(r.text)
# do note that the post/put probably requires a json.
# in that case, create a payload = {'key1': 'value1' ...}
# then: requests.put(<url>, params = payload)
# see more at http://www.python-requests.org/en/latest/user/quickstart/

# r = requests.get("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'))
# print(r.text)
# r = requests.delete("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'), params = {'m_id': '3', 'p_id': '2'})
# print(r.text)
# r = requests.post("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'), params = {'m_id': '10', 'p_id': '10'})
# print(r.text)
# r = requests.get("http://localhost:5000/schedule", auth = HTTPBasicAuth('admin','password'))
# print(r.text)
#


# r = requests.post("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'), params = {'start_time': '1300', 'end_time': '1900', 'location': "toilet"})
# print(r.text)
# r = requests.get("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
# print(r.text)
# r = requests.put("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'), params = {'start_time': '1300', 'end_time': '2000', 'location': "Junshengs Room"})
# print(r.text)
# r = requests.get("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
# print(r.text)
# # r = requests.delete("http://localhost:5000/meeting/1337", auth = HTTPBasicAuth('admin','password'))
# # print(r.text)

# r = requests.post("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'), params = {'name': 'cool dude', 'timetable': '1000-1900'})
# print(r.text)
# r = requests.put("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'), params = {'name': 'Stanley', 'timetable': '1000-2100'})
# print(r.text)
# r = requests.get("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
# print(r.text)
# r = requests.delete("http://localhost:5000/person/1337", auth = HTTPBasicAuth('admin','password'))
# print(r.text)