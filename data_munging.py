import pandas as pd
import json

with open('theme_transportation.json', 'r') as file:
   transport = json.load(file)
   data = transport['result']['results']

# data is 10 records long
tags = {}
for result in data:
    for tag in result['tags']:
        print(tag['name'])
        if tag['name'] in tags:
            tags[tag['name']] += 1
        else:
            tags[tag['name']] = 1

print(tags)
