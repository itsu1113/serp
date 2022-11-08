from common.common_rakuten import *

@click.command('task_rakuten_spapi', help="Hello World.") 
@with_appcontext
def task_rakuten_spapi_run():
    # output()
    # driver=get_driver()
    # jan_code = driver.find_element(By.ID, "rakujan-wrapper").get_attribute('data-rakujan-jan')
    # print(get_rnk_list())
    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_'+process_date+'.tsv'

    # ランキングリスト
    rnk_list=get_rnk_list()
    # webdriver
    driver=get_driver()

    # ランキングリストをループ
    is_first=True
    for rnk in rnk_list:
        logger.debug('--start '+ rnk['code'])
        # 結果リスト
        result_list=list()
        
        # Webページを取得して解析する
        html=requests.get(rnk['url'])
        soup=BeautifulSoup(html.text,'html.parser')
        items=soup.find_all(class_='rnkRanking_itemName')

        # タブに商品を表示させる
        open_tab(items, driver)

        # 開いているタブから利益率とURLを取得。結果に反映
        add_result_list(driver, result_list)
        
        # 開いているタブが１つになるまで閉じる
        close_tab(driver)
        
        # アマゾン出品許可チェック
        chek_approved(driver, result_list)

        # ３ヶ月販売数チェック
        chek_sales(driver, result_list)
        print(result_list)
        # 結果リストを成形
        if len(result_list)==0:
            continue
            
        print('--start '+ rnk['code'])
        for result in result_list:
            result['rnk_code']=rnk['code']
            # 結果行を１行出力する。
            row_str=''
            for k in result.keys():
                row_str+=result[k]
                row_str+='\t'
            # print(row_str)

        # 結果リストをCSV出力
        with open("C:\\Users\\ItsukiSato\\Documents\\20_TOOL\\rakuten_files\\"+file_name, 'a', newline="", encoding='UTF-8') as f:
            fieldnames = result_list[0].keys()
            writer     = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
            if is_first:
                writer.writeheader()
                is_first=False
            for result in result_list:
                writer.writerow(result)

# ランキングコードリストを定義
def get_rnk_list():
    # ランキングリスト
    rnk_list=list(range(0))
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
            surl=item.a.get("href")
            # URLを開き、新しいタブを開く
            driver.switch_to.window(driver.window_handles[tab_idx])
            driver.get(surl)
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

# 想定利益を計算_楽天
def add_result_list(driver, result_list):
    for window in driver.window_handles:
        try:
            driver.switch_to.window(window)
            jan_code             = driver.find_element(By.ID, "rakujan-wrapper").get_attribute('data-rakujan-jan')
            catalog              = get_catalog(jan_code)
            rakuzon_asin         = catalog['ASIN']
            if rakuzon_asin == '':
                continue
            rakuzon_cart         = get_price(rakuzon_asin)
            if rakuzon_cart == 0:
                continue
            rakuzon_imgTitle     = catalog['Title']
            rakuzon_price        = int(driver.find_element(By.ID, "priceCalculationConfig").get_attribute("data-price"))
            basic_point          = get_basic_point(driver)
            other_point          = 7
            expecte_point        = rakuzon_price*(basic_point+other_point)/100
            actual_purchase_price= rakuzon_price-expecte_point
            fee                  = get_fee(rakuzon_asin)
            rakuzon_profit       = rakuzon_cart-actual_purchase_price-fee
            profit_per           = round(rakuzon_profit/rakuzon_cart*100,1)
            if float(profit_per) > 5 \
            and is_sold(driver)==False:
                result_list.append({'profit':str(profit_per), 'asin':rakuzon_asin, 'rakuzon_price':str(rakuzon_price), 'rakuzon_imgTitle':rakuzon_imgTitle,\
                                    'rakuzon_cart':str(rakuzon_cart), 'url':driver.current_url})

        except Exception as e:
            print('Exception add_result_list')
            print(driver.current_url)
            print(e)
            continue







