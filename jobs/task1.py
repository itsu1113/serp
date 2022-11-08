import click
from flask.cli import with_appcontext
# from models import db
from common.common_rakuten import *

from logger import logger
driver=get_driver()
@click.command('task1', help="Hello World.") # コマンドから「flask job taskNN」の形で実行する際の名称taskNN を第１引数に書く
@with_appcontext
def task1_run():
    a=get_price(driver)
    print(a)

def get_price(driver):
    try:
        price = driver.find_element(By.CSS_SELECTOR, "#productInfo > div.productInfoArea > p > span.price").get_attribute("content")
        price = int(price)
        return price
    except Exception as e:
        try:
            price = driver.find_element(By.CSS_SELECTOR, "#productInfo > div.productInfoArea > p > span:nth-child(6)").get_attribute("content")
            price = int(price)
            return price
        except Exception as e:
            try:
                price = int(driver.find_element(By.ID, "priceCalculationConfig").get_attribute("data-price"))
                return price
            except Exception as e:
                return '-'
