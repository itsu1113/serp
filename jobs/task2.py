import click
from flask.cli import with_appcontext
from models import db

from logger import logger

from selenium import webdriver
from time import sleep

@click.command('task2', help="Hello World.") # コマンドから「flask job taskNN」の形で実行する際の名称taskNN を第１引数に書く
@with_appcontext
def task2_run():
    print("hello world!!!")


    # DB select (SQLを直接書く例)
    users = db.select('select * from users where id = %s', [1])
    print(users)

    # DB select (Query Builderを使用する例)
    users = db.table('users').where('id', 1).get()
    print(users)
    for user in users:
        print(user)

    # log (logger.py 中のLOGFILEに出力)
    logger.debug(vars(users))

    # # seleniumの利用
    # driver = webdriver.Chrome('/path/to/chromedriver') 
    # driver.get('https://www.google.co.jp')
    # submit = driver.find_element_by_name('btnK')
    # print(submit.get_attribute('value'))