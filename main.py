import concurrent.futures
import multiprocessing
import os
import sys

import tqdm as tq
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup as bs
import requests
import re
import json
import time
import math
from fake_useragent import UserAgent
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

    def normal_crawl(self, i, mall, url, conf, headers, d):
        # target mall, url
        html = requests.get(url, headers=headers).text
        bsObject = bs(html, "lxml")
        product_name = bsObject.find("meta", {"property": "og:" + conf[mall]['productName'] + ""})['content']
        data = re.search(conf[mall]['jsonRegex'], html, re.S).group(1)
        json_data = json.loads(data)
        origin_price = json_data[conf[mall]['originPrice']]
        sale_price = json_data[conf[mall]['salePrice']]
        if origin_price == sale_price:
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
        d[i] = {"index": i, "target": mall, "url": url, "productName": product_name,
                "originPrice": origin_price,
                "salePrice": sale_price, "discountPercent": discount_percent}

        return d[i]

    def emart_crawl(self, i, mall, url, d):
        ua = UserAgent()
        userAgent = ua.random
        headers = {'User-Agent': userAgent}
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        html = requests.get(url, headers=headers, proxies=proxies).text
        bsObject = bs(html, "lxml")
        try:
            product_name = bsObject.find("meta", {"property": "og:title"})['content']
            origin_price = bsObject.find("input", {"id": "sellprc"})["value"]
            sale_price = bsObject.find("input", {"id": "sellUnitPrc"})["value"]

        except:
            b = re.search(r'bestAmt:parseInt\(\'(.*?)\',', html, re.S).group(1)
            origin_price = b
            sale_price = None
            discount_percent = None
        if origin_price == sale_price:
            discount_percent = None
            sale_price = None
        elif origin_price != sale_price and origin_price or sale_price is not None:
            discount_percent = math.trunc(100 * (1 - (int(sale_price) / int(origin_price))))

        d[i] = {"index": i, "target": mall, "url": url, "productName": product_name,
                "originPrice": origin_price,
                "salePrice": sale_price, "discountPercent": discount_percent}
        return d[i]

    def detail(self, file_name, t):
        global mall, url
        # redefining 4 convenience
        target = self.target
        conf = self.conf
        headers = self.headers

        # dictionary 4 output.json
        d = {}
        d_error = {}

        # defining 4 tqdm
        progress_bar = tq.tqdm(t, desc=file_name)
        for i, _ in zip(t, progress_bar):
            progress_bar.refresh()
            i = str(i)
            mall = target[i]["target"]
            url = target[i]["url"]
            try:
                if mall == 'emart':
                    self.emart_crawl(i, mall, url, d)
                else:
                    self.normal_crawl(i, mall, url, conf, headers, d)
            except Exception as e:
                d_error[i] = {"target": mall, "url": url, "error": e}
                pass
        # ensure_ascii = False -> The letters are printed as they are. (To prevent cracking of Korean letters.)
        json.dump(d, open(file_name + ".json", "w"), ensure_ascii=False)
        json.dump(d_error, open(file_name + "error.json", "w"), ensure_ascii=False)

    def json_combine(self):
        z = {}
        for i in range(10, 0, -1):
            i = str(i) + ".json"
            z = json.load(open(i)) | z
            if os.path.isfile(i):
                os.remove(i)
        json.dump(z, open('output.json', 'w'), ensure_ascii=False)
        z = {}
        for i in range(10, 0, -1):
            i = str(i) + "error.json"
            z = json.load(open(i)) | z
            if os.path.isfile(i):
                os.remove(i)
        json.dump(z, open('error.json', 'w'), ensure_ascii=False)

    def run(self, object):
        a = len(self.target) // 10
        th1 = Process(target=object.detail, args=("1", range(0, a)))
        th2 = Process(target=object.detail, args=("2", range(a, 2 * a)))
        th3 = Process(target=object.detail, args=("3", range(2 * a, 3 * a)))
        th4 = Process(target=object.detail, args=("4", range(3 * a, 4 * a)))
        th5 = Process(target=object.detail, args=("5", range(4 * a, 5 * a)))
        th6 = Process(target=object.detail, args=("6", range(5 * a, 6 * a)))
        th7 = Process(target=object.detail, args=("7", range(6 * a, 7 * a)))
        th8 = Process(target=object.detail, args=("8", range(7 * a, 8 * a)))
        th9 = Process(target=object.detail, args=("9", range(8 * a, 9 * a)))
        th10 = Process(target=object.detail, args=("10", range(9 * a, 10 * a + 1)))

        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th5.start()
        th6.start()
        th7.start()
        th8.start()
        th9.start()
        th10.start()
        th1.join()
        th2.join()
        th3.join()
        th4.join()
        th5.join()
        th6.join()
        th7.join()
        th8.join()
        th9.join()
        th10.join()
        self.json_combine()


if __name__ == '__main__':
    start_time = time.time()
    shop = ShoppingDetail()
    shop.run(shop)
    print(time.time() - start_time)
