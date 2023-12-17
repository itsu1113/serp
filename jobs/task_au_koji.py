from common.common import *

# webdriver
driver=get_driver()

@click.command('task_au_koji', help="Hello World.") 
@with_appcontext
def task_au_koji_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_au_koji'+process_date+'.tsv'
    # ランキングリスト
    cate_list=get_cate_list()
    fieldnames=[]
    is_first=True

    for category in cate_list:
        logger.debug('--start '+ category)
        base_url="https://wowma.jp/itemlist?categ_id="+category+"&spe_id=list_nav_prc&clow=5000&chigh=&user=43478324"
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
    cate_list.append("53")
    cate_list.append("46")
    cate_list.append("44")
    cate_list.append("41")
    return cate_list

def get_jan1():
    try:
        jan_code=''
        sentence=driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/section/section/div[3]/div[3]/section/div/div[1]/div/div')[0].get_attribute("innerHTML")
        target = 'JANコード：'
        idx = sentence.find(target)
        jan_code = sentence[idx+7:idx+20]
        
        return jan_code
    except Exception as e:
        return '-'
    
def get_price():
    try:
        try:
            price = driver.find_element(By.CLASS_NAME, 'Price_price__currentPrice__FaSZR.false').text.replace(',', '').replace('円(税込)', '')
        except NoSuchElementException:
            price = driver.find_element(By.CLASS_NAME, 'Price_price__currentPrice__FaSZR.Price_price__currentPrice_sale__tmcHk').text.replace(',', '').replace('円(税込)', '')
        return int(price)
    except Exception as e:
        return 0

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
   
def get_item(result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue

            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(result['item_url'])
            time.sleep(1.5)
            
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

            # 実質仕入値
            point=get_point()
            price=get_price()
            actual_price=price-(price/1.1*(point*0.01))
            result['item_price']= round(actual_price)

        except NoSuchElementException as e:
            result['invalid']=1
            print(e)
            continue
        except Exception as e:
            result['invalid']=1
            print(e)
            continue
            
def get_point():
    try:
        point=driver.find_element(By.CLASS_NAME, "ReductionDetails_reduction__contents_rate__GEFFj").get_attribute('innerHTML').replace('(', '').replace('%)', '')
        return float(point)
    except Exception as e:
        return 0


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
