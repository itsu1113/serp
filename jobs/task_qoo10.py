from common.common import *

# webdriver
driver=get_driver()

@click.command('task_qoo10', help="Hello World.") 
@with_appcontext
def task_qoo10_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_q10'+process_date+'.tsv'
    # ランキングリスト
    cate_list=get_cate_list()

    fieldnames=[]
    is_first=True
    for category in cate_list:
        logger.debug('--start '+ category)
        base_url="https://www.qoo10.jp/gmkt.inc/Bestsellers/?g="+category

        item_list_page=base_url
        driver=get_driver()
        driver.get(item_list_page)

        # ページから商品urlを取得しshohin_listへ格納
        shohin_list = []
        looplist_items = driver.find_elements(By.CLASS_NAME, 'item') 
        for l in looplist_items:
            atags = l.find_elements(By.TAG_NAME, "a")
            for atag in atags:
                shohin_list.append(atag.get_attribute("href"))
                break


        for shohin in shohin_list:
            # 結果リスト
            result_list=list()
            result_list.append({'invalid':0, 'category':category, 'item_url':shohin})

            # 商品情報取得
            get_item(driver, result_list)
            
            # リーファ情報取得
            get_leafer(driver, result_list)

            # 利益計算を行う
            calc_profit(result_list)

            # アマゾン出品許可チェック
            chek_approved(driver, result_list)

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

# カテゴリリストを定義
def get_cate_list():
    # ランキングリスト
    cate_list=list(range(0))
    cate_list.append("4")
    cate_list.append("14")
    return cate_list

def get_jan1():
    try:
        jan_code=driver.find_element(By.XPATH, '//*[@id="tr_pan_industry"]/td').text
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
        item_price=driver.find_element(By.ID, "sp_max_dc_price").text.replace(",", "")
        return item_price
    except Exception as e:
        return '-'
    
def get_price2():
    try:
        item_price=driver.find_elements(By.CLASS_NAME, 'elPriceNumber')[0].get_attribute('innerHTML').replace(',', '').replace('円', '')
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
        point_per=driver.find_elements(By.CLASS_NAME, 'elGetRate')[0].get_attribute('innerHTML').replace('\n', '').replace('%獲得', '').replace(' ', '')
        point_per=round(float(point_per)*0.01, 3)
        return point_per
    except Exception as e:
        return '-'

def get_point_per0():
    try:
        point_per=driver.find_elements(By.CLASS_NAME, 'elTotalRateText')[0].get_attribute('innerHTML').replace('\n', '').replace('%獲得', '').replace(' ', '')
        point_per=round(float(point_per)*0.01, 3)
        return point_per
    except Exception as e:
        return '-'
    
def get_point_per1():
    try:
        point_per=driver.find_elements(By.CLASS_NAME, 'ItemPointHeader_rate')[0].get_attribute('innerHTML').replace('%', '')
        point_per=float(point_per)*0.01
        return point_per
    except Exception as e:
        return '-'
    
def get_point_per2():
    try:
        point_per=driver.find_elements(By.CLASS_NAME, 'elTotalRateRate')[0].get_attribute('innerHTML').replace('%', '')
        point_per=float(point_per)*0.01
        return point_per
    except Exception as e:
        return '-'

def get_item(driver, result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue

            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(result['item_url'])
            time.sleep(0.5)
            
            # jan_code
            jan_code=get_jan1()
            if jan_code=='-':
                # jan_code=get_jan2()
                if jan_code=='-':
                    result['invalid']=1
                    continue
            
            # jan_code書式チェック
            if check_jan(jan_code):
                result['jan_code']=jan_code
            else:
                result['jan_code']=9999999999999
                result['invalid']=1
                continue
                
            # 獲得ポイント％
            # point_per=get_point_per00()
            # if point_per=='-':
            #     point_per=get_point_per0()
            #     if point_per=='-':
            #         point_per=get_point_per1()
            #         if point_per=='-':
            #             point_per=get_point_per2()
            #             if point_per=='-':
            #                 result['jan_code']=9999999999998
            #                 result['invalid']=1
            #                 continue

            # 仕入値
            item_price=get_price1()
            if item_price=='-':
                # item_price=get_price2()
                if item_price=='-':
                    result['invalid']=1
                    continue
            result['item_price']=int(item_price)

        except NoSuchElementException as e:
            result['invalid']=1
            print(e)
            continue
        except Exception as e:
            result['invalid']=1
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
            gross_profit = float(result['bunkiten']) - float(result['item_price'])
            result['gross_profit'] = gross_profit

            # 粗利率
            gross_profit_per = round(gross_profit / float(result['cart']) * 100, 1)
            result['gross_profit_per'] = gross_profit_per

            if gross_profit_per < 1:
                result['invalid'] = 1

            # 販売数
            sales_volume = int(result['sales_volume'])
            if sales_volume < 5:
                result['invalid'] = 1

        except Exception as e:
            result['invalid'] = 1
            print('Exception calc_profit')
            print(result)
            print(e)
            continue


