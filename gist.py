#!/usr/bin/python3
from github import Github
import os
import json
import requests
from pprint import pprint

content = open("gist.txt", "r").read() # create a text file to hold all the code you intend to share     
token = Github_Api_Key = os.environ["GITHUB_TOKEN"] # github api token
g = Github(token)
query_url = "https://api.github.com/gists"
data = {
    "public": False, # i have my gists private by default
    "description": input("\nEnter a short description of the gist\n> "),
    "files": {
        input("\nEnter name of the file for gist\n> "): {
            "content": "{}".format(content)
        },
    }
}
headers = {'Authorization': f'token {token}'}
response = requests.post(query_url, headers=headers, data=json.dumps(data))
pprint(response.json())