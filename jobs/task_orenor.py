import click
from flask.cli import with_appcontext
from common.common import *
from logger import logger
driver=get_driver()
@click.command('task_orenor', help="Hello World.") 
@with_appcontext
def task_orenor_run():
    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_orenor'+process_date+'.tsv'

    fieldnames=[]
    is_first=True
    base_url="https://orenoraresne.com/page/"
    # p1-p3までをループする
    for i in range(1, 4):
        driver.get(base_url+str(i))

        # 結果リスト
        result_list = []

        items=driver.find_elements(By.CLASS_NAME, 'post-list__link')
        for item in items:
            result_list.append({'invalid':0, 'title':item.get_attribute("title"), 'item_url':item.get_attribute("href")})

        # 商品情報取得
        get_item(driver, result_list)

        # 結果リストをCSV出力
        with open("C:\\serp\\files\\"+file_name, 'a', newline="", encoding='UTF-8') as f:
            if is_first:
                for result in result_list:
                    if result['invalid'] == 0:
                        fieldnames = result.keys()
                        writer     = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
                        writer.writeheader()
                        is_first=False
                        break
            else:
                writer = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)

            for result in result_list:
                if result['invalid'] == 0:
                    try:
                        writer.writerow(result)
                    except Exception as e:
                        print(result)
                        print(e)
                        continue

def get_item(driver, result_list):
    for result in result_list:
        try:

            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(result['item_url'])
            time.sleep(0.5)
            price_content=get_price_content(driver)
            result['price_content']=price_content


        except Exception as e:
            result['invalid']=1
            print(e)
            continue


def get_price_content(driver):
    try:
        cboxcomments=driver.find_elements(By.CLASS_NAME, 'cboxcomment')
        # print(cboxcomments)
        for cboxcomment in cboxcomments:
            try:
                target=cboxcomment.find_element(By.CLASS_NAME, 'has-text-align-center').get_attribute('innerHTML')
            except Exception as e:
                continue
            
            if '俺的プレ値' in target:
                return target.replace('<strong>', '').replace('</strong>', '')

    except Exception as e:
        return 'error'