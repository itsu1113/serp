from common.common import *

# webdriver
driver=get_driver()

@click.command('task_au', help="Hello World.") 
@with_appcontext
def task_au_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_au'+process_date+'.tsv'
    # ランキングリスト
    cate_list=get_cate_list()
    fieldnames=[]
    is_first=True


    for category in cate_list:
        logger.debug('--start '+ category)
        base_url="https://wowma.jp/itemlist?categ_id="+category+"&spe_id=list_nav_prc&clow=3000&chigh="
        # p1-p10までをループする
        for i in range(1, 10):
            item_list_page=base_url+"&page="+str(i)+"&clk="+str(i)
            driver.get(item_list_page)
            shohin_list = driver.find_elements(By.CLASS_NAME, "productMainColumn")
            # wk結果リスト
            result_list = []
            cnt=0
            for shohin in shohin_list:
                result_list.append({'invalid':0, 'category':category, 'item_url':shohin.get_attribute("href")})
    
            # 商品情報取得
            get_item(result_list)

            # リーファ情報取得
            get_leafer(driver, result_list)

            # 利益計算を行う
            calc_profit(result_list)

                # for result in result_list:
                #     print(result)

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
    cate_list.append("403405")
    cate_list.append("53")
    cate_list.append("46")
    cate_list.append("29")
    cate_list.append("35")
    cate_list.append("44")
    cate_list.append("41")
    cate_list.append("33")
    cate_list.append("34")
    cate_list.append("31")
    cate_list.append("54")
    cate_list.append("40")
    cate_list.append("42")
    cate_list.append("49")
    cate_list.append("52")
    cate_list.append("56")
    cate_list.append("59")
    return cate_list

def get_jan1():
    try:
        jan_code=''
        links = driver.find_elements(By.CSS_SELECTOR, "link")
        for link in links:
            if link.get_attribute("rel") == 'canonical':
                jan_url=link.get_attribute("href")
                jan_code=re.search(r'\d+', jan_url).group()
        return jan_code
    except Exception as e:
        return '-'
    
def get_price1():
    try:
        item_price=driver.find_element(By.ID, "js-baseItemPrice").get_attribute("innerHTML").replace(',', '')
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
    
def get_point_per1():
    try:
        point_per = driver.find_element(By.CSS_SELECTOR, "#js-accordionToggle > li > div > div.uniTriggerItem.js-accordion-trigger.js-item-scroll-trigger > a > span > span:nth-child(2)")
        point_per = point_per.get_attribute("innerHTML").replace('\n', '').replace('%', '').replace(' ', '').replace('（', '').replace('）', '')
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
    
def get_item(result_list):
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
                result['invalid']=1
                continue

            # jan書式チェック
            if check_jan(jan_code):
                result['jan_code']=jan_code
            else:
                result['jan_code']=9999999999999
                result['invalid']=1
                continue

            # 獲得ポイント％
            point_per=get_point_per1()
            if point_per=='-':
                result['jan_code']=9999999999998
                result['invalid']=1
                continue

            # 仕入値
            item_price=get_price1()
            if item_price=='-':
                result['invalid']=1
                continue
            result['item_price']=int(item_price)-(int(item_price)*point_per)

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
                # gross_profit_per+=15 #test
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


