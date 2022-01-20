import json, time
from bs4 import BeautifulSoup as bs
import requests
import re

# # interpark
# html = requests.get("https://shopping.interpark.com/product/productInfo.do?prdNo=8572663480").text
# bsObject = bs(html, "html.parser")
#
# # print
# data = re.search('var __EGS_DATAOBJ=(.*?);', html, re.S).group(1)
# print(bsObject.find("meta", {"property": "og:title"})['content'])
# print(title.text)
# print(json.loads(data)['sale_price'])
# print(json.loads(data)['item_price'])

# 11st

# html = requests.get("https://www.11st.co.kr/products/1690152883").text
# bsObject = bs(html, "html.parser")

# print
# data = re.search('var productPrdInfo = (.*?);', html, re.S).group(1)
# print(html)
# print(bsObject.find("meta", {"property": "og:title"})['content'])
# print(json.loads(data)['selPrc'])
# print(json.loads(data)['finalDscPrc'])
# print(html)


# g9 가격정보 크롤링 불가
# html = requests.get("https://www.g9.co.kr/Display/VIP/Index/2333090493").text
# bsObject = bs(html, "html.parser")
#
# # print
# # data = re.search('var productPrdInfo = (.*?);', html, re.S).group(1)
# print(html)
# print(bsObject.find('title').text)
# # print(json.loads(data)['selPrc'])
# # print(json.loads(data)['finalDscPrc'])
# # print(html)

# wemakeprice
# html = requests.get("https://front.wemakeprice.com/product/2010257167").text
# bsObject = bs(html, "html.parser")
#
# data = re.search(r',"sale":(.*?),"shipDispYn"', html, re.S).group(1)
# print(bsObject.find("meta", {"property": "og:title"})['content'])
#
# print(json.loads(data)['salePrice'])
# print(json.loads(data)['originPrice'])
# print(json.loads(data)['discountRate'])

# gsshop
# start = time.time()
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
# html = requests.get(
#     "http://with.gsshop.com/prd/prd.gs?prdid=33804878&lseq=390725-8&gsid=ECmain-AU390725-AU390725-8&dseq=8&svcid=pc&bnclick=main-mrcm_mainMrcmW_apiBytedanceEx&rank=8",
#     headers=headers).text
# bsObject = bs(html, "html.parser")
# data = re.search(r'{"prc":(.*?),"gftExistFlg"', html, re.S).group(1)
#
# print(bsObject.find("meta", {"property": "og:title"})['content'])
# print(json.loads(data)['salePrc'])
# print(json.loads(data)['minPrc'])
# print(json.loads(data)['dcRate'])
# print(time.time() - start)

#tmon
# start = time.time()
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
# html = requests.get(
#     "http://www.tmon.co.kr/deal/9575361718",
#     headers=headers).text
# bsObject = bs(html, "html.parser")
# data = re.search(r'"priceInfo":(.*?),"priceMeta"', html, re.S).group(1)
# print(bsObject.find("meta", {"property": "og:title"})['content'])
# print(json.loads(data)['price'])
# print(json.loads(data)['originalPrice'])
# print(json.loads(data)['discountRate'])
# print(time.time() - start)


# cjonstyle 불가
# start = time.time()
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
# html = requests.get(
#     "https://display.cjonstyle.com/p/mocode/M1152085",
#     headers=headers).text
# bsObject = bs(html, "html.parser")
# print(bsObject.find("meta", {"property": "og:description"})['content'])
# print(html)
# # data = re.search(r'"priceInfo":(.*?),"priceMeta"', html, re.S).group(1)
# print(json.loads(data)['price'])
# print(json.loads(data)['originalPrice'])
# print(json.loads(data)['discountRate'])
# print(time.time() - start)

# skstoa
start = time.time()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
html = requests.get(
    "http://www.skstoa.com/display/goods/25187098?prdListCode=%ED%99%88_%EC%B6%94%EC%B2%9C%EC%83%81%ED%92%88%3E%EC%83%81%ED%92%88",
    headers=headers).text
bsObject = bs(html, "html.parser")
print(bsObject.find("meta", {"property": "og:description"})['content'])
# print(html)
try:
    print(bsObject.select_one('#goodsView > div.goods_upper.clearfix > div.right > div.right_cont > div.cont_tit > div.lower.clearfix > div.l_part > p.price > strong').text.replace("\n", ""))
    print(bsObject.select_one('#goodsView > div.goods_upper.clearfix > div.right > div.right_cont > div.cont_tit > div.lower.clearfix > div.l_part > p.origin').text.replace(" ", "").replace("원", "").replace("\n", ""))
    print(bsObject.select_one('#goodsView > div.goods_upper.clearfix > div.right > div.right_cont > div.cont_tit > div.lower.clearfix > div.l_part > p.sale').text)
except:
    print(bsObject.select_one('#contents > div:nth-child(2) > div.goods_upper.clearfix > div.right > div.right_cont > div.cont_tit > div.lower.clearfix > div > p > strong').text)
    print(0)
    print(0)
print(time.time() - start)

# emart
