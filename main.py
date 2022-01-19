import json
import tqdm as tq
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class ShoppingDetail:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.wait = WebDriverWait(self.driver, 60)
        self.target = json.load(open("target.json"))
        self.conf = json.load(open("conf.json"))

    def detail(self):
        global mall
        driver = self.driver
        wait = self.wait
        conf = self.conf
        target = self.target
        count = 1
        d = {}
        t = tq.trange(1, len(target))
        for i, _ in zip(target, t):
            try:
                mall = target[i]["target"]
                url = conf[mall]["url"] + target[i]["product_id"]

                t.set_description("[Current target : %s]" % mall)
                t.refresh()

                driver.get(url)
                product_name = wait.until(EC.presence_of_element_located((By.XPATH, conf[mall]["productName"]))).text
                origin_price = driver.find_element(By.XPATH, conf[mall]["originPrice"]).text
                if conf[mall]["salePrice"] == "":
                    sale_price = None
                else:
                    sale_price = driver.find_element(By.XPATH, conf[mall]["salePrice"]).text
                if conf[mall]["discountPercent"] == "":
                    discount_percent = None
                else:
                    discount_percent = driver.find_element(By.XPATH, conf[mall]["discountPercent"]).text
                d[count] = {"target": mall, "url": url, "productName": product_name, "originPrice": origin_price,
                            "salePrice": sale_price, "discountPercent": discount_percent}
                count += 1
            except NoSuchElementException or TimeoutException:
                count += 1
                print(mall, " Error")
        json.dump(d, open("output.json", "w"), ensure_ascii=False)


shop = ShoppingDetail()
shop.detail()
