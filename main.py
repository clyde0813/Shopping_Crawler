import tqdm as tq
from multiprocessing import Process
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import os
import requests
import re
import json
import time
import math


class ShoppingDetail:
    def __init__(self):
        # target.json load
        self.target = json.load(open("target.json"))
        # conf.jons load
        self.conf = json.load(open("conf.json"))
        # headers
        self.ua = UserAgent()
        self.userAgent = self.ua.random
        self.headers = {'User-Agent': self.userAgent}

        # selenium webdriver
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("User-Agent:" + self.userAgent)
        self.options.add_argument("headless")
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager.install()), options=self.options)

    def text_filter(self, o, s, d):
        if type(o) is str:
            o = int(o.replace(",", "").replace("원", ""))
        if type(s) is str:
            s = int(s.replace(",", "").replace("원", ""))
        if type(d) is str:
            d = int(d.replace("%", ""))
        return o, s, d

    def normal_crawl(self, i, mall, url, headers, conf, d):
        # target mall, url
        html = requests.get(url, headers=headers).text
        bsObject = bs(html, "lxml")
        try:
            product_name = bsObject.find("meta", {"property": "og:" + conf[mall]['productName']})['content']
        except:
            product_name = bsObject.find(conf[mall]['productName']).text
        data = re.search(conf[mall]['jsonRegex'], html, re.S).group(1)
        try:
            json_data = json.loads(data)
        except:
            data = data.replace("//Optional", "") + "}"
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
        text_filter = self.text_filter(origin_price, sale_price, discount_percent)
        # adding data to dictionary
        d[i] = {"index": int(i), "target": mall, "url": url, "productName": product_name,
                "originPrice": text_filter[0],
                "salePrice": text_filter[1], "discountPercent": text_filter[2]}

        return d[i]

    def auction_crawl(self, i, mall, url, headers, conf, d):
        html = requests.get(url, headers=headers).text
        bsObject = bs(html, "lxml")
        try:
            product_name = bsObject.find("meta", {"property": "og:" + conf[mall]['productName'] + ""})['content']
            origin_price = bsObject.find("span", {conf[mall]["originPrice"][0]: conf[mall]["originPrice"][1]}).text
            sale_price = bsObject.find("strong", {conf[mall]["salePrice"][0]: conf[mall]["salePrice"][1]}).text
            discount_percent = bsObject.find("strong",
                                             {conf[mall]["discountPercent"][0]: conf[mall]["discountPercent"][1]}).text
        except:
            product_name = bsObject.find("meta", {"property": "og:" + conf[mall]['productName'] + ""})['content']
            try:
                origin_price = bsObject.find("span",
                                             {conf[mall]["originPrice"][0]: conf[mall]["originPrice"][3]}).text.replace(
                    "								",
                    "").replace("\n", "")
            except:
                origin_price = bsObject.find("strong", {conf[mall]["salePrice"][0]: conf[mall]["salePrice"][1]}).text
            sale_price = None
            discount_percent = None
        # adding data to dictionary
        text_filter = self.text_filter(origin_price, sale_price, discount_percent)
        # adding data to dictionary
        d[i] = {"index": int(i), "target": mall, "url": url, "productName": product_name,
                "originPrice": text_filter[0],
                "salePrice": text_filter[1], "discountPercent": text_filter[2]}

        return d[i]

    def gmarket_crawl(self, i, mall, url, headers, conf, d):
        html = requests.get(url, headers=headers).text
        bsObject = bs(html, "lxml")
        product_name = bsObject.find("meta", {"property": "og:" + conf[mall]['productName']})['content']
        origin_price = re.search(conf[mall]['originPrice'], html, re.S).group(1)
        sale_price = re.search(conf[mall]['salePrice'], html, re.S).group(1)
        discount_percent = None
        if origin_price == sale_price:
            sale_price = None
            discount_percent = None
        elif origin_price is not sale_price and sale_price is not None:
            discount_percent = math.trunc(100 * (1 - (int(sale_price) / int(origin_price))))
        text_filter = self.text_filter(origin_price, sale_price, discount_percent)
        # adding data to dictionary
        d[i] = {"index": int(i), "target": mall, "url": url, "productName": product_name,
                "originPrice": text_filter[0],
                "salePrice": text_filter[1], "discountPercent": text_filter[2]}

        return d[i]

    def lotteimall_crawl(self, i, mall, url, headers, conf, d):
        html = requests.get(url, headers=headers).text
        bsObject = bs(html, "lxml")
        product_name = bsObject.find("meta", {"property": "og:" + conf[mall]["productName"]})['content']
        origin_price = re.search(conf[mall]["originPrice"], html, re.S).group(1)
        sale_price = bsObject.find("meta", {"property": "og:" + conf[mall]["salePrice"]})['content']
        if origin_price == "0":
            origin_price = sale_price
            sale_price = None
            discount_percent = None
        elif origin_price == sale_price:
            sale_price = None
            discount_percent = None
        else:
            try:
                discount_percent = math.trunc(100 * (1 - (int(sale_price) / int(origin_price))))
            except:
                discount_percent = None
            if discount_percent == 0:
                discount_percent = None
        # adding data to dictionary
        text_filter = self.text_filter(origin_price, sale_price, discount_percent)
        d[i] = {"index": int(i), "target": mall, "url": url, "productName": product_name,
                "originPrice": text_filter[0],
                "salePrice": text_filter[1], "discountPercent": text_filter[2]}
        return d[i]

    def selenium_crawl(self, i, mall, url, headers, conf, d):
        driver = self.driver
        driver.get(url)

    def detail(self, file_name, t):
        # redefining 4 convenience
        target = self.target
        conf = self.conf
        headers = self.headers
        status_code = None
        # dictionary 4 output.json
        d = {}
        d_error = {}

        # defining 4 tqdm
        progress_bar = tq.tqdm(t, position=0, desc=file_name)
        for i, _ in zip(t, progress_bar):
            progress_bar.refresh()
            i = str(i)
            mall = target[i]["target"]
            url = target[i]["url"]
            try:
                if mall == "emart":
                    pass
                elif mall == "auction":
                    self.auction_crawl(i, mall, url, headers, conf, d)
                elif mall == "gmarket":
                    self.gmarket_crawl(i, mall, url, headers, conf, d)
                elif mall == "lotteimall":
                    self.lotteimall_crawl(i, mall, url, headers, conf, d)
                else:
                    self.normal_crawl(i, mall, url, headers, conf, d)
            except Exception as e:
                d_error[i] = {"target": mall, "url": url, "error": str(e), "status_code": status_code}

        # ensure_ascii = False -> The letters are printed as they are. (To prevent cracking of Korean letters.)
        json.dump(d, open(file_name + ".json", "w"), ensure_ascii=False)
        json.dump(d_error, open(file_name + "error.json", "w"), ensure_ascii=False)

    def json_combine(self):
        z = {}
        for i in range(16, 0, -1):
            i = str(i) + ".json"
            z = json.load(open(i)) | z
            if os.path.isfile(i):
                os.remove(i)
        json.dump(z, open('output.json', 'w'), ensure_ascii=False)
        z = {}
        for i in range(16, 0, -1):
            i = str(i) + "error.json"
            z = json.load(open(i)) | z
            if os.path.isfile(i):
                os.remove(i)
        json.dump(z, open('error.json', 'w'), ensure_ascii=False)

    def run(self, object):
        a = len(self.target) // 15
        b = len(self.target) - (15 * a)
        th1 = Process(target=object.detail, args=("1", range(0, a)))
        th2 = Process(target=object.detail, args=("2", range(a, 2 * a)))
        th3 = Process(target=object.detail, args=("3", range(2 * a, 3 * a)))
        th4 = Process(target=object.detail, args=("4", range(3 * a, 4 * a)))
        th5 = Process(target=object.detail, args=("5", range(4 * a, 5 * a)))
        th6 = Process(target=object.detail, args=("6", range(5 * a, 6 * a)))
        th7 = Process(target=object.detail, args=("7", range(6 * a, 7 * a)))
        th8 = Process(target=object.detail, args=("8", range(7 * a, 8 * a)))
        th9 = Process(target=object.detail, args=("9", range(8 * a, 9 * a)))
        th10 = Process(target=object.detail, args=("10", range(9 * a, 10 * a)))
        th11 = Process(target=object.detail, args=("11", range(10 * a, 11 * a)))
        th12 = Process(target=object.detail, args=("12", range(11 * a, 12 * a)))
        th13 = Process(target=object.detail, args=("13", range(12 * a, 13 * a)))
        th14 = Process(target=object.detail, args=("14", range(13 * a, 14 * a)))
        th15 = Process(target=object.detail, args=("15", range(14 * a, 15 * a)))
        th16 = Process(target=object.detail, args=("16", range(15 * a, 15 * a + b)))
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
        th11.start()
        th12.start()
        th13.start()
        th14.start()
        th15.start()
        th16.start()

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
        th11.join()
        th12.join()
        th13.join()
        th14.join()
        th15.join()
        th16.join()
        self.json_combine()


if __name__ == '__main__':
    start_time = time.time()
    shop = ShoppingDetail()
    shop.run(shop)
    print(time.time() - start_time)
    error = json.load(open("error.json"))
    success = json.load(open("output.json"))
    print("Error count : %d\nSuccess count : %d" % (len(error), len(success)))
