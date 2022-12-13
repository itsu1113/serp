from common.common_rakuten import *

@click.command('task_get_arari', help="Hello World.") 
@with_appcontext
def task_get_arari_run():
    try:
        # 処理日
        process_date = datetime.datetime.now().strftime('%Y%m%d')
        # 出力ファイル名
        file_name='research_get_arari'+process_date+'.tsv'
        # webdriver
        driver=get_driver()
        fieldnames=[]
        input_list=[]
        is_first=True
        f = open("C:\\serp\\files\\input\\1col.tsv", 'r', encoding='UTF-8')
        for data in f:
            input_list.append(data.rstrip('\n'))
        f.close()

        for asin in input_list:
            # 結果リスト
            result_list=list()

            result_list.append({'invalid':0, 'asin':asin})

            # リーファ情報取得
            get_leafer_asin(driver, result_list)
            
            # アクセス制限対策
            # time.sleep(7)

            # 結果リストをCSV出力
            with open("C:\\serp\\files\\"+file_name, 'a', newline="", encoding='UTF-8') as f:
                if is_first==True:
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
    except Exception as e:
        print(e)
