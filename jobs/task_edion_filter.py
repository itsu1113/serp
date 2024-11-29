from common.common_rakuten import *

@click.command('task_edion_filter', help="Hello World.") 
@with_appcontext
def task_edion_filter_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d')
    # 出力ファイル名
    file_name='research_edion_filter_'+process_date+'.tsv'

    # webdriver
    driver=get_driver()
    fieldnames=[]
    input_list=[]

    f = open("C:\\serp\\files\\input\\1col.tsv", 'r', encoding='UTF-8')
    for data in f:
        input_list.append(data.rstrip('\n'))
    f.close()

    is_first=True
    for jan_code in input_list:

        # 結果リスト
        result_list=list()
        result_list.append({'invalid':0, 'jan_code':jan_code})
        
        # リーファ情報取得
        get_leafer(driver, result_list)

        # アクセス制限対策
        time.sleep(10)
        
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


# 利益計算を行う
def calc_profit(result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue

            # 販売数
            sales_volume = int(result['sales_volume'])
            if sales_volume < 5:
                result['invalid'] = 1

            # 損益分岐点
            bunkiten = int(result['bunkiten'])
            if bunkiten > 60000:
                result['invalid'] = 1
            if bunkiten < 4000:
                result['invalid'] = 1

        except Exception as e:
            result['invalid'] = 1
            print('Exception calc_profit')
            print(result)
            print(e)
            continue


