import click
from flask.cli import with_appcontext
# from models import db
from common.common_rakuten import *

api = keepa.Keepa(accesskey)

from logger import logger
driver=get_driver()
@click.command('task1', help="Hello World.") # コマンドから「flask job taskNN」の形で実行する際の名称taskNN を第１引数に書く
@with_appcontext
def task1_run():

    test = get_basic_point(driver)
    print(test)
    # products = api.query('B07HRXW5PM') # returns list of product data
    # product_parms = {
    #     "current_SALES_gte": 1,
    #     "current_SALES_lte": 3000,
    #     "avg30_SALES_gte": 1,
    #     "avg30_SALES_lte": 60000,
    #     "deltaPercent90_AMAZON_gte": -1000,
    #     "deltaPercent90_AMAZON_lte": -30,
    #     "current_COUNT_NEW_gte": 2,
    #     "avg30_COUNT_NEW_gte": 3,
    #     "productType": [
    #         0,
    #         1
    #     ],
    #     "page": 0,
    #     "perPage": 50
    # }
    # asins = api.product_finder(product_parms,domain='JP')
    # products = api.query(asins,domain='JP')
    # print('ASIN is ' + products[0]['asin'])
    # print('Title is ' + products[0]['title'])

    
    # logger.debug(products[0]['type'])
    # logger.debug(products[0]['rootCategory'])
    

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
