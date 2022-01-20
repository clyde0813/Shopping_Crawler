import os
import sys

import tqdm as tq
from bs4 import BeautifulSoup as bs
import requests
import re
import json
import time
import math
import threading


class ShoppingDetail:
    def __init__(self):
        # bypass detection
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

        # target.json load
        self.target = json.load(open("target.json"))
        # conf.jons load
        self.conf = json.load(open("conf.json"))

    def detail(self):
        global mall, url

        # redefining 4 convenience
        target = self.target
        conf = self.conf
        headers = self.headers

        # dictionary 4 output.json
        d = {}
        d_error = {}

        # defining 4 tqdm
        t = range(len(target))

        for i in t:
            # try:
            # target mall, url
            i = str(i)
            mall = target[i]["target"]
            url = target[i]["url"]
            print(mall, url)
            html = requests.get(url, headers=headers).text
            bsObject = bs(html, "lxml")

            product_name = bsObject.find("meta", {"property": "og:" + conf[mall]['productName'] + ""})['content']

            data = re.search(conf[mall]['jsonRegex'], html, re.S).group(1)
            json_data = json.loads(data)
            origin_price = json_data[conf[mall]['originPrice']]
            sale_price = json_data[conf[mall]['salePrice']]
            if origin_price == sale_price and conf[mall]['discountPercent'] == "":
                discount_percent = None
                sale_price = None
            elif origin_price != sale_price and conf[mall]['discountPercent'] == "":
                discount_percent = math.trunc(100 * (1 - (int(sale_price) / int(origin_price))))
            elif origin_price is None and sale_price is not None:
                origin_price = sale_price
                sale_price = None
                discount_percent = None
            else:
                discount_percent = json_data[conf[mall]['discountPercent']]

            # adding data to dictionary
            d[i] = {"index": i, "target": mall, "url": url, "productName": product_name, "originPrice": origin_price,
                    "salePrice": sale_price, "discountPercent": discount_percent}

            # If the element you are looking for is not found or the page does not exist
            # except Exception as e:
            #     d_error[i] = {"reason": e, "target": mall, "url": url}
            #     print("\n", mall, " : ", e)

            # ensure_ascii = False -> The letters are printed as they are. (To prevent cracking of Korean letters.)
        json.dump(d, open("output" + ".json", "w"), ensure_ascii=False)
        json.dump(d_error, open("error.json", "w"), ensure_ascii=False)

    # def json_combine(self):
    #     files = ['5.json', '4.json', '4.json', '3.json', '2.json', '1.json']
    #     z = {}
    #     for i in files:
    #         z = json.load(open(i)) | z
    #
    #     json.dump(z, open('output.json', 'w'), ensure_ascii=False)
    #     for i in files:
    #         if os.path.isfile(i):
    #             os.remove(i)

    # def run(self, object):
    #     target = self.target
    #     a = 11 + len(target) // 5
    #     th1 = threading.Thread(target=object.detail, args=("1", 11, a))
    #     th2 = threading.Thread(target=object.detail, args=("2", a, 2 * a))
    #     th3 = threading.Thread(target=object.detail, args=("3", 2 * a, 3 * a))
    #     th4 = threading.Thread(target=object.detail, args=("4", 3 * a, 4 * a))
    #     th5 = threading.Thread(target=object.detail, args=("5", 4 * a, 5 * a))
    #     th1.start()
    #     th2.start()
    #     th3.start()
    #     th4.start()
    #     th5.start()
    #     th1.join()
    #     th2.join()
    #     th3.join()
    #     th4.join()
    #     th5.join()
    #     # self.json_combine()


start_time = time.time()
shop = ShoppingDetail()
shop.detail()
print(time.time() - start_time)
