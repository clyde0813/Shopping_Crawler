import json

target = json.load(open('target.json'))
a = len(target) // 5
print(a)