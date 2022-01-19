import json

target = [
    "interpark",
    "11st",
    "g9",
    "wemakeprice",
    "gsshop",
    "tmon",
    "cjonstyle",
    "skstoa",
    "emart",
    "ssg",
    "auction",
    "gmarket",
    "lotteon",
    "galleria",
    "lotteimall",
    "coupang"
]
product_id = [
    "8175645813",
    "3316729314",
    "1963411775",
    "626204072",
    "68685524",
    "8955420326",
    "94362774",
    "24508138",
    "1000289080220",
    "1000031768784",
    "B862259465",
    "1824842698",
    "LO1589639179",
    "2112366248",
    "12698185",
    "160531013"
]
print(len(target), len(product_id))
tmp = {}
count = 1
for i, j in zip(target, product_id):
    tmp[count] = {'target': i, 'product_id': j}
    count += 1
json.dump(tmp, open('target.json', 'w'))


