from common.common_rakuten import *

@click.command('task_rakuten_keyword', help="Hello World.") 
@with_appcontext
def task_rakuten_keyword_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_rakuten_keyword'+process_date+'.tsv'

    # アクセス制限URLリスト
    restrict_urls=[]
    fieldnames=[]
    # キーワード
    keyword='楽天ブックス'
    base_url="https://search.rakuten.co.jp/search/mall/"+keyword+"/?p="

    # p1-p28までをループする
    is_first=True
    for i in range(1, 28):
        item_list_page=base_url+str(i)
        # webdriver なぜかループ毎にgetする必要あり
        driver=get_driver()
        driver.get(item_list_page)

        logger.debug('--start '+ str(i))
        # 結果リスト
        result_list=list()
        
        elems = driver.find_elements(By.CSS_SELECTOR, '#root > div.dui-container.main > div.dui-container.content > div.dui-container.searchresults > div')[0].find_elements(By.CSS_SELECTOR, "div.content.title > h2 > a")
        # 各商品URLをリスト化
        items = [] 
        for elem in elems:
            items.append(elem.get_attribute("href"))

        # タブに商品を表示させる
        open_tab(items, driver)

        # 開いているタブから利益率とURLを取得。結果に反映
        get_rakuten(driver, result_list, restrict_urls)

        # 開いているタブが１つになるまで閉じる
        close_tab(driver)
        
        # アクセス制限リストが10件以下になるまで再試行する
        while len(restrict_urls) > 10:
            print(len(restrict_urls))
            open_tab(restrict_urls, driver)
            restrict_urls=[]
            get_rakuten(driver, result_list, restrict_urls)
            close_tab(driver)

        # リーファ情報取得
        get_leafer(driver, result_list)

        # 利益計算を行う
        calc_profit(result_list)

        # アマゾン出品許可チェック
        chek_approved(driver, result_list)

        # for result in result_list:
        #     print(result)

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

# リストのURLをタブに表示する
def open_tab(items, driver):
    tab_idx=0
    for item in items:
        try:
            # URLを開き、新しいタブを開く
            driver.switch_to.window(driver.window_handles[tab_idx])
            driver.get(item)
            driver.execute_script("window.open('https://www.google.com');")
            time.sleep(2)
            tab_idx=tab_idx+1
            # if tab_idx==5:
            #     break #test
            time.sleep(7)#アクセス制限対策
        except Exception as e:
            print('Exception:'+'open_tab')
            print(e)
            continue

# 価格を取得
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

# 楽天表示情報を取得
def get_rakuten(driver, result_list, restrict_urls):
    for window in driver.window_handles:
        try:
            driver.switch_to.window(window)
            jan_code             = driver.find_element(By.ID, "rakujan-wrapper").get_attribute('data-rakujan-jan')
            rakuzon_price        = get_price(driver)
            basic_point          = get_basic_point(driver)
            other_point          = 7
            expecte_point        = rakuzon_price*(basic_point+other_point)/100
            actual_purchase_price= rakuzon_price-expecte_point
            result_list.append({'invalid':0, 'jan_code':str(jan_code), 'rakuzon_price':str(rakuzon_price), 'basic_point':str(basic_point),\
                                'actual_purchase_price':actual_purchase_price,'url':driver.current_url})
        except NoSuchElementException as e:
            print(e)
            try:
                errorTxt = driver.find_element(By.TAG_NAME, "h2").get_attribute("innerHTML")
                if errorTxt=='アクセスが集中し、ページを閲覧しにくい状態になっております':
                    restrict_urls.append(driver.current_url)
                continue
            except NoSuchElementException as e:
                try:
                    errorTxt = driver.find_element(By.TAG_NAME, "h1").get_attribute("innerHTML")
                    if errorTxt=='Access Denied':
                        print('Access Denied発生')
                        restrict_urls.append(driver.current_url)
                        time.sleep(180)
                    continue
                except Exception as e:
                    print(e)
                    continue
            except Exception as e:
                print(e)
                continue
        except Exception as e:
            print('Exception get_rakuten')
            print(driver.current_url)
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
            gross_profit = float(result['bunkiten']) - float(result['actual_purchase_price'])
            result['gross_profit'] = gross_profit

            # 粗利率
            gross_profit_per = round(gross_profit / float(result['cart']) * 100, 1)
            result['gross_profit_per'] = gross_profit_per

            if gross_profit_per < -10:
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


