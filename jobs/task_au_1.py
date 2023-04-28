from common.common import *

@click.command('task_au_1', help="Hello World.") 
@with_appcontext
def task_au_1_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d')
    # 出力ファイル名
    file_name='research_au_1_'+process_date+'.tsv'

    # webdriver
    driver=get_driver()
    fieldnames=[]
    # 結果リスト
    result_list=list()

    # 開いているタブから実質仕入値、型番を取得。結果に反映
    get_item_info(driver, result_list)

    # 開いているタブが１つになるまで閉じる
    close_tab(driver)

    # 結果リストをCSV出力
    with open("C:\\serp\\files\\"+file_name, 'a', newline="", encoding='UTF-8') as f:
        for result in result_list:
            if result['invalid'] == 0:
                fieldnames = result.keys()
                writer     = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
                writer.writeheader()
                break
        for result in result_list:
            if result['invalid'] == 0:
                try:
                    writer.writerow(result)
                except Exception as e:
                    print(result)
                    print(e)
                    continue

# 表示情報を取得
def get_item_info(driver, result_list):
    for window in driver.window_handles:
        try:
            driver.switch_to.window(window)
            actual_purchase_price = driver.find_element(By.ID, "actual_price").get_attribute('value')
            title = driver.find_element(By.CLASS_NAME, "ItemTitle_itemTitle__xB1b2").text

            result_list.append({'invalid':0, 'url':driver.current_url, 'actual_purchase_price':actual_purchase_price, 'title':title})
        except Exception as e:
            print('Exception get_item_info')
            print(driver.current_url)
            print(e)
            continue

