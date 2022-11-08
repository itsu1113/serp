from common.common_rakuten import *

@click.command('task_edion', help="Hello World.") 
@with_appcontext
def task_edion_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d')
    # 出力ファイル名
    file_name='research_edion'+process_date+'.tsv'

    # webdriver
    driver=get_driver()
    fieldnames=[]
    # 結果リスト
    result_list=list()

    # 開いているタブから利益率とURLを取得。結果に反映
    get_rakuten(driver, result_list)

    # 開いているタブが１つになるまで閉じる
    close_tab(driver)
    
    # リーファ情報取得
    get_leafer(driver, result_list)

    # 利益計算を行う
    calc_profit(result_list)

    # アマゾン出品許可チェック
    chek_approved(driver, result_list)

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

# 楽天表示情報を取得
def get_rakuten(driver, result_list):
    for window in driver.window_handles:
        try:
            driver.switch_to.window(window)
            jan_code             = driver.find_element(By.ID, "rakujan-wrapper").get_attribute('data-rakujan-jan')
            rakuzon_price        = int(driver.find_element(By.ID, "priceCalculationConfig").get_attribute("data-price"))
            basic_point          = get_basic_point(driver)
            other_point          = 7
            expecte_point        = rakuzon_price*(basic_point+other_point)/100
            actual_purchase_price= rakuzon_price-expecte_point
            result_list.append({'invalid':0, 'jan_code':str(jan_code), 'rakuzon_price':str(rakuzon_price), 'basic_point':str(basic_point), \
                                'actual_purchase_price':actual_purchase_price, 'url':driver.current_url})
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

            if gross_profit_per < 7:
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


