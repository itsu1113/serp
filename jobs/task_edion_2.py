from common.common_rakuten import *

@click.command('task_edion_2', help="Hello World.") 
@with_appcontext
def task_edion_2_run():
    is_first=True
    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d')
    # 出力ファイル名
    file_name='research_edion_2_'+process_date+'.tsv'

    # webdriver
    driver=get_driver()
    fieldnames=[]
    # 結果リスト
    result_list_rak=list()

    # tsvから楽天情報取得
    get_rakuten(driver, result_list_rak)

    for result_row in result_list_rak:
        result_list=list()
        result_list.append(result_row)
        # リーファ情報取得
        get_leafer(driver, result_list)

        # 利益計算を行う
        calc_profit(result_list)

        # アマゾン出品許可チェック
        chek_approved(driver, result_list)

        # 結果リストをCSV出力
        with open("C:\\serp\\files\\"+file_name, 'a', newline="", encoding='UTF-8') as f:
            for result in result_list:
                if is_first:
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
    # アクセス制限対策
    time.sleep(5)
    
# 楽天表示情報を取得
def get_rakuten(driver, result_list):
    try:
        input_list=[]
        with open('C:\\serp\\files\\input\\3col.tsv', encoding='utf-8', newline='') as f:
            for cols in csv.reader(f, delimiter='\t'):
                input_list.append(cols)
        for item in input_list:
                url                  = item[0]
                jan_code             = item[1]
                other_point          = 7
                actual_purchase_price= item[2]
                result_list.append({'invalid':0, 'jan_code':str(jan_code),\
                                    'actual_purchase_price':actual_purchase_price, 'url':url})
    except Exception as e:
        print(e)

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

            if gross_profit_per < 6:
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


