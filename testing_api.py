# Name: testing_api.py
# Description: Simple testing suite for the API.
import requests

r = requests.get("http://localhost:5000/")
print(r.text)
r = requests.get("http://localhost:5000/meeting")
print(r.text)
r = requests.get("http://localhost:5000/person")
print(r.text)
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