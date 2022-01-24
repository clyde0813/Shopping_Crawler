import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
conf = json.load(open('conf.json'))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument(
    'User-Agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://display.cjonstyle.com/p/item/46253209?channelCode=30001001")
html = driver.page_source
bsObject = bs(html, "lxml")
mall = 'cjonstyle'
# print(bsObject)
print(conf[mall]["productName"][0])
product_name = \
bsObject.find(conf[mall]["productName"][0], {conf[mall]["productName"][1]: conf[mall]["productName"][2]})["content"]
try:
    print(conf[mall]["originPrice"][0])
    origin_price = bsObject.select_one("#sDPrice2").text
except:
    origin_price = bsObject.select_one(conf[mall]["originPrice"][1]).text
try:
    sale_price = bsObject.find(conf[mall]["salePrice"]).text
except:
    sale_price = None
try:
    discount_percent = bsObject.find(conf[mall]["discountPercent"]).text
except:
    discount_percent = None

print(origin_price, sale_price, discount_percent)