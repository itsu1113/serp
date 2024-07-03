from common.common_rakuten import *

@click.command('task_rakuten', help="Hello World.") 
@with_appcontext
def task_rakuten_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_rakuten'+process_date+'.tsv'

    # ランキングリスト
    rnk_list=get_rnk_list()
    # webdriver
    driver=get_driver()
    # アクセス制限URLリスト
    restrict_urls=[]

    fieldnames=[]

    # ランキングリストをループ
    is_first=True
    for rnk in rnk_list:
        logger.debug('--start '+ rnk['code'])
        # 結果リスト
        result_list=list()
        
        # Webページを取得して解析する
        # html=requests.get(rnk['url'])
        # soup=BeautifulSoup(html.text,'html.parser')
        # items=soup.find_all(class_='rnkRanking_itemName')
        driver.get(rnk['url'])
        elems = driver.find_elements(By.CLASS_NAME, 'rnkRanking_itemName')

        # 各商品URLをリスト化
        items = [] 
        for elem in elems:
            items.append(elem.find_element(By.TAG_NAME, "a").get_attribute("href"))

        # タブに商品を表示させる
        open_tab(items, driver)

        # 開いているタブから利益率とURLを取得。結果に反映
        get_rakuten(driver, result_list, restrict_urls)

        # 開いているタブが１つになるまで閉じる
        close_tab(driver)
        
        # アクセス制限リストが10件以下になるまで再試行する
        while len(restrict_urls) > 10:
            time.sleep(300)# test 5分間待機
            print(len(restrict_urls))
            open_tab2(restrict_urls, driver)
            restrict_urls=[]
            get_rakuten(driver, result_list, restrict_urls)
            close_tab(driver)

        # リーファ情報取得
        get_leafer(driver, result_list)

        # 利益計算を行う
        calc_profit(result_list)

        # アマゾン出品許可チェック
        chek_approved(driver, result_list)

        print('--start '+ rnk['code'])

        # 結果リストをCSV出力
        with open("C:\\serp\\files\\"+file_name, 'a', newline="", encoding='UTF-8') as f:
            if is_first:
                for result in result_list:
                    if result['invalid'] == 0:
                        fieldnames = result.keys()
                        writer     = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
                        writer.writeheader()
                        is_first=False
                        # break
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

# ランキングコードリストを定義
def get_rnk_list():
    # ランキングリスト
    rnk_list=list(range(0))
    rnk_list.append({'code':"204586"}) # 炊飯器
    rnk_list.append({'code':"550932"}) # BLレコーダー
    rnk_list.append({'code':"201912"}) # リール
    rnk_list.append({'code':"100087"})
    rnk_list.append({'code':"553158"})
    rnk_list.append({'code':"100212"})
    rnk_list.append({'code':"110105"})
    rnk_list.append({'code':"100103"})
    rnk_list.append({'code':"110080"})
    rnk_list.append({'code':"213619"})
    rnk_list.append({'code':"567167"})
    rnk_list.append({'code':"208287"})
    rnk_list.append({'code':"507524"})
    rnk_list.append({'code':"213517"})
    rnk_list.append({'code':"211741"})
    rnk_list.append({'code':"207609"})
    rnk_list.append({'code':"507513"})
    rnk_list.append({'code':"100644"})
    rnk_list.append({'code':"100890"})
    rnk_list.append({'code':"203107"})
    rnk_list.append({'code':"204183"})
    rnk_list.append({'code':"101165"})
    rnk_list.append({'code':"566385"})
    rnk_list.append({'code':"100558"})
    rnk_list.append({'code':"567168"})
    rnk_list.append({'code':"101916"})
    rnk_list.append({'code':"206024"})
    rnk_list.append({'code':"100094"})
    rnk_list.append({'code':"213401"})
    rnk_list.append({'code':"565751"})
    rnk_list.append({'code':"560062"})
    rnk_list.append({'code':"201912"})
    rnk_list.append({'code':"200169"})
    rnk_list.append({'code':"201890"})
    rnk_list.append({'code':"509057"})
    rnk_list.append({'code':"568560"})
    rnk_list.append({'code':"206213"})
    rnk_list.append({'code':"400817"})
    rnk_list.append({'code':"201916"})
    rnk_list.append({'code':"111355"})
    rnk_list.append({'code':"551256"})
    rnk_list.append({'code':"204228"})
    rnk_list.append({'code':"200225"})
    rnk_list.append({'code':"101126"})
    rnk_list.append({'code':"566384"})
    rnk_list.append({'code':"200305"})
    rnk_list.append({'code':"563843"})
    rnk_list.append({'code':"111961"})
    rnk_list.append({'code':"214668"})
    rnk_list.append({'code':"565750"})
    rnk_list.append({'code':"207622"})
    rnk_list.append({'code':"204200"})
    rnk_list.append({'code':"201959"})
    rnk_list.append({'code':"211307"})
    rnk_list.append({'code':"212988"})
    rnk_list.append({'code':"208582"})
    rnk_list.append({'code':"562640"})
    rnk_list.append({'code':"101737"})
    rnk_list.append({'code':"558945"})
    rnk_list.append({'code':"205263"})
    rnk_list.append({'code':"402486"})
    rnk_list.append({'code':"111475"})
    rnk_list.append({'code':"213684"})
    rnk_list.append({'code':"560029"})
    rnk_list.append({'code':"101168"})
    rnk_list.append({'code':"566383"})
    rnk_list.append({'code':"100984"})
    rnk_list.append({'code':"303087"})
    rnk_list.append({'code':"563338"})
    rnk_list.append({'code':"213198"})
    rnk_list.append({'code':"112998"})
    rnk_list.append({'code':"407735"})
    rnk_list.append({'code':"100893"})
    rnk_list.append({'code':"201963"})
    rnk_list.append({'code':"101739"})
    rnk_list.append({'code':"211233"})
    rnk_list.append({'code':"502823"})
    rnk_list.append({'code':"566735"})
    rnk_list.append({'code':"503249"})
    rnk_list.append({'code':"553203"})
    rnk_list.append({'code':"202952"})
    rnk_list.append({'code':"101876"})
    rnk_list.append({'code':"100901"})
    rnk_list.append({'code':"101451"})
    rnk_list.append({'code':"201955"})
    rnk_list.append({'code':"101914"})
    rnk_list.append({'code':"565699"})
    rnk_list.append({'code':"215298"})
    rnk_list.append({'code':"566955"})
    rnk_list.append({'code':"111519"})
    rnk_list.append({'code':"205246"})
    rnk_list.append({'code':"100155"})
    rnk_list.append({'code':"110247"})
    rnk_list.append({'code':"201950"})
    rnk_list.append({'code':"205074"})
    rnk_list.append({'code':"560198"})
    rnk_list.append({'code':"112779"})
    rnk_list.append({'code':"201591"})
    rnk_list.append({'code':"559275"})
    rnk_list.append({'code':"567750"})
    rnk_list.append({'code':"503285"})
    rnk_list.append({'code':"100872"})
    rnk_list.append({'code':"204210"})
    rnk_list.append({'code':"553765"})
    rnk_list.append({'code':"567273"})
    rnk_list.append({'code':"567843"})
    rnk_list.append({'code':"213656"})
    rnk_list.append({'code':"213731"})
    rnk_list.append({'code':"408507"})
    rnk_list.append({'code':"210238"})
    rnk_list.append({'code':"100191"})
    rnk_list.append({'code':"201603"})
    rnk_list.append({'code':"564895"})
    rnk_list.append({'code':"101975"})
    rnk_list.append({'code':"560202"})
    rnk_list.append({'code':"566115"})
    rnk_list.append({'code':"567219"})
    rnk_list.append({'code':"206139"})
    rnk_list.append({'code':"112913"})
    rnk_list.append({'code':"100762"})
    rnk_list.append({'code':"203018"})
    rnk_list.append({'code':"553789"})
    rnk_list.append({'code':"404237"})
    rnk_list.append({'code':"302472"})
    rnk_list.append({'code':"111469"})
    rnk_list.append({'code':"553769"})
    rnk_list.append({'code':"200170"})
    rnk_list.append({'code':"100629"})
    rnk_list.append({'code':"204745"})
    rnk_list.append({'code':"566114"})
    rnk_list.append({'code':"564992"})
    rnk_list.append({'code':"203260"})
    rnk_list.append({'code':"100863"})
    rnk_list.append({'code':"502046"})
    rnk_list.append({'code':"112928"})
    rnk_list.append({'code':"210167"})
    rnk_list.append({'code':"565162"})
    rnk_list.append({'code':"201775"})
    rnk_list.append({'code':"206023"})
    rnk_list.append({'code':"100805"})
    rnk_list.append({'code':"101859"})
    rnk_list.append({'code':"406700"})
    rnk_list.append({'code':"565054"})
    rnk_list.append({'code':"568199"})
    rnk_list.append({'code':"565739"})
    rnk_list.append({'code':"213749"})
    rnk_list.append({'code':"203020"})
    rnk_list.append({'code':"565063"})
    rnk_list.append({'code':"100857"})
    rnk_list.append({'code':"566954"})
    rnk_list.append({'code':"563727"})
    rnk_list.append({'code':"551942"})
    rnk_list.append({'code':"100656"})
    rnk_list.append({'code':"559248"})
    rnk_list.append({'code':"565164"})
    rnk_list.append({'code':"100554"})
    rnk_list.append({'code':"100645"})
    rnk_list.append({'code':"101893"})
    rnk_list.append({'code':"111981"})
    rnk_list.append({'code':"553755"})
    rnk_list.append({'code':"567436"})
    rnk_list.append({'code':"205279"})
    rnk_list.append({'code':"505948"})
    rnk_list.append({'code':"567525"})
    rnk_list.append({'code':"563818"})
    rnk_list.append({'code':"560050"})
    rnk_list.append({'code':"111524"})
    rnk_list.append({'code':"213647"})
    rnk_list.append({'code':"407057"})
    rnk_list.append({'code':"566068"})
    rnk_list.append({'code':"100933"})
    rnk_list.append({'code':"100987"})
    rnk_list.append({'code':"560276"})
    rnk_list.append({'code':"111363"})
    rnk_list.append({'code':"565163"})
    rnk_list.append({'code':"567751"})
    rnk_list.append({'code':"101100"})
    rnk_list.append({'code':"565749"})
    rnk_list.append({'code':"100012"})
    rnk_list.append({'code':"566386"})



    for rnk in rnk_list:
        rnk['url']="https://ranking.rakuten.co.jp/daily/"+rnk['code']+"/"
        
    return rnk_list

# ランキングの商品をループし、タブに表示させる
def open_tab(items, driver):
    tab_idx=0
    for item in items:
        try:
            # 商品URLを取得
            # surl=item.find_element(By.TAG_NAME, "a").get_attribute("href")

            # URLを開き、新しいタブを開く
            driver.switch_to.window(driver.window_handles[tab_idx])
            driver.get(item)
            driver.execute_script("window.open('https://www.google.com');")
            time.sleep(2)
            tab_idx=tab_idx+1
            # if tab_idx==5:
            #     break
                
        except NoSuchElementException as e:
            print('NoSuchElementException:'+'open_tab')
            print(e)
            continue
        except Exception as e:
            print('Exception:'+'open_tab')
            print(e)
            continue

# リストのURLをタブに表示する
def open_tab2(items, driver):
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
            #     break
                
        except Exception as e:
            print('Exception:'+'open_tab')
            print(e)
            continue

# 楽天表示情報を取得
def get_rakuten(driver, result_list, restrict_urls):
    for window in driver.window_handles:
        try:
            driver.switch_to.window(window)
            jan_code             = get_jan_code(driver)
            rakuzon_price        = get_price(driver)
            basic_point          = get_basic_point(driver)
            other_point          = 3
            expecte_point        = rakuzon_price*(basic_point+other_point)/100
            actual_purchase_price= rakuzon_price-expecte_point
            result_list.append({'invalid':0, 'jan_code':str(jan_code), 'rakuzon_price':str(rakuzon_price), 'basic_point':str(basic_point),\
                                'actual_purchase_price':actual_purchase_price,'url':driver.current_url})
        except NoSuchElementException as e:
            try:
                errorTxt = driver.find_element(By.TAG_NAME, "h2").get_attribute("innerHTML")
                if errorTxt=='アクセスが集中し、ページを閲覧しにくい状態になっております':
                    restrict_urls.append(driver.current_url)
                continue
            except Exception as e:
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

            if gross_profit_per < 5:
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


