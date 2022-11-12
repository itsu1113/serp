import click
from flask.cli import with_appcontext
from common.common import *
from logger import logger
driver=get_driver()
@click.command('task_get_current_price', help="Hello World.") 
@with_appcontext
def task_get_current_price_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    driver=get_driver()
    is_first=True

    # 開いているタブをループ
    for i in range(0, len(driver.window_handles)):
        try:
            driver.switch_to.window(driver.window_handles[i])
            # 結果リスト初期化
            result_list=list()

            # 開いているタブから価格を取得
            current_price=driver.find_element(By.ID,'MainContent_txt_SalesPlanPrice').get_attribute("value")
            asin=driver.find_element(By.ID,'MainContent_lbl_Asin').get_attribute("value")
            result_list.append({'current_price':current_price, 'asin':asin})

            # 結果リストを成形
            if len(result_list)==0:
                continue

            for result in result_list:
                # 結果行を１行出力する。
                row_str=''
                for k in result.keys():
                    row_str+=result[k]
                    row_str+='\t'
                print(row_str)

        except Exception as e:
            print(e)
            continue