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
        # Chrome WebDriver Options
        self.options = webdriver.ChromeOptions()

        # headless & etc
        self.options.add_argument("headless")
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")

        # bypass detection
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        # driver definition
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        # 60sec wait
        self.wait = WebDriverWait(self.driver, 30)

        # target.json load
        self.target = json.load(open("target.json"))

        # conf.jons load
        self.conf = json.load(open("conf.json"))

    def detail(self):
        # 4 exception
        global mall, url
        # redefining 4 convenience
        driver = self.driver
        wait = self.wait
        conf = self.conf
        target = self.target

        # dictionary 4 output.json
        d = {}
        d_error = {}

        # defining 4 tqdm
        t = tq.trange(1, len(target))

        for i, _ in zip(target, t):
            try:
                # target mall, url
                mall = target[i]["target"]
                url = conf[mall]["url"] + target[i]["product_id"]

                # tqdm message
                t.set_description("[Current target : %s]" % mall)
                t.refresh()

                driver.get(url)

                product_name = wait.until(EC.presence_of_element_located((By.XPATH, conf[mall]["productName"]))).text
                origin_price = driver.find_element(By.XPATH, conf[mall]["originPrice"]).text

                # For shopping malls that do not offer discounts
                if conf[mall]["salePrice"] == "":
                    sale_price = None
                else:
                    sale_price = driver.find_element(By.XPATH, conf[mall]["salePrice"]).text
                if conf[mall]["discountPercent"] == "":
                    discount_percent = None
                else:
                    discount_percent = driver.find_element(By.XPATH, conf[mall]["discountPercent"]).text

                # adding data to dictionary
                d[i] = {"target": mall, "url": url, "productName": product_name, "originPrice": origin_price,
                        "salePrice": sale_price, "discountPercent": discount_percent}

            # If the element you are looking for is not found or the page does not exist
            except NoSuchElementException:
                d_error[i] = {"reason": "NoSuchElementException", "target": mall,
                              "product_id": target[i]["product_id"], "url": url}
                print("\n", mall, " : No Such Element Exception")
            except TimeoutException:
                d_error[i] = {"reason": "TimeoutException", "target": mall,
                              "product_id": target[i]["product_id"], "url": url}
                print("\n", mall, " : Timeout Exception")

        # ensure_ascii = False -> The letters are printed as they are. (To prevent cracking of Korean letters.)
        json.dump(d, open("output.json", "w"), ensure_ascii=False)
        json.dump(d_error, open("error.json", "w"), ensure_ascii=False)


shop = ShoppingDetail()
shop.detail()
