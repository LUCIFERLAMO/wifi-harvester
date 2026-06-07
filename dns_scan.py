import requests

base_url = "https://api.github.com/users"

# get the profile of user torvalds
name = "torvalds"
ts = requests.get(f"{base_url}/{name}")

if ts.status_code != 200:
    print(f"request failed {ts.status_code}")
else:
    response = ts.json()
    print(response["name"])
    print(response["public_repos"])
    print(response["followers"])
    print(response["location"])

name1 = "nonexistentuser99999 "

result = requests.get(f"{base_url}/{name1}")
if result.status_code != 200:
    print(f"user not found {result.status_code}")