from common.common import *
# webdriver
driver=get_driver()

@click.command('task_yahoo_resale', help="Hello World.") 
@with_appcontext
def task_yahoo_resale_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_ys_resale'+process_date+'.tsv'

    fieldnames=[]
    # 結果リスト
    result_list = list()

    # 開いているタブから商品情報取得
    get_item(driver, result_list)

    # 開いているタブが１つになるまで閉じる
    close_tab(driver)

    # リーファ情報取得
    get_mori(driver, result_list)

    # 利益計算を行う
    calc_profit(result_list)

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

def get_jan1():
    try:
        jan_code=driver.find_element(By.CSS_SELECTOR, "#itm_cat > tbody > tr:nth-child(2) > td").get_attribute('innerHTML')
        return jan_code
    except Exception as e:
        return '-'
    
def get_jan2():
    try:
        jan_code=driver.find_element(By.CSS_SELECTOR, "#itm_cat > ul > li:nth-child(2) > div.elRowData > p").get_attribute('innerHTML')
        return jan_code
    except Exception as e:
        return '-'
    
def get_price1():
    try:
        item_price=driver.find_elements(By.CLASS_NAME, 'styles_price__7WGwS')[0].text.replace(',', '').replace('円', '')
        return item_price
    except Exception as e:
        return '-'
    
def get_price2():
    try:
        item_price=driver.find_elements(By.CLASS_NAME, 'elPrice')[0].get_attribute('innerText').replace(',', '').replace('円', '')
        return item_price
    except Exception as e:
        return '-'
    
def check_jan(jan_code):
    try:
        jan_code=str(jan_code)
        if jan_code.isnumeric():
            if len(jan_code)==13:
                return True
        return False
    except Exception as e:
        print(e)
        return False

def get_point_per00():
    try:
        point_per=driver.find_elements(By.CLASS_NAME, 'styles_pointRatio__EepZ3')[0].text.replace('\n', '').replace('%獲得', '').replace(' ', '')
        point_per=round(float(point_per)*0.01, 3) #取得できなかった場合キャストの際にexceptionになる
        return point_per
    except Exception as e:
        return '-'

def get_item(driver, result_list):
    for window in driver.window_handles:
        try:
            driver.switch_to.window(window)
            # jan_code
            jan_code=get_jan1()
            if jan_code=='-':
                jan_code=get_jan2()
                if jan_code=='-':
                    jan_code=1111
            
            # jan_code書式チェック
            if check_jan(jan_code):
                jan_code=jan_code
            else:
                jan_code=2222
                
            # 獲得ポイント％
            point_per=get_point_per00()
            if point_per=='-':
                point_per=0
                            
            # 仕入値
            item_price=get_price1()
            if item_price=='-':
                item_price=get_price2()
                if item_price=='-':
                    item_price=0
            actual_purchase_price=int(item_price)-(int(item_price)*point_per)

            result_list.append({'invalid':0, 'item_price':str(item_price), 'point_per':str(point_per),\
                                'url':driver.current_url, 'jan_code':str(jan_code), 'actual_purchase_price':actual_purchase_price,\
                                })
        except NoSuchElementException as e:
            print(e)
            continue
        except Exception as e:
            print(e)
            continue

# 利益計算を行う
def calc_profit(result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue

            # 粗利
            gross_profit = float(result['mori_price']) - float(result['actual_purchase_price'])
            result['gross_profit'] = gross_profit

            # 粗利率
            gross_profit_per = round(gross_profit / float(result['mori_price']) * 100, 1)
            result['gross_profit_per'] = gross_profit_per


        except Exception as e:
            result['invalid'] = 1
            print('Exception calc_profit')
            print(result)
            print(e)
            continue


