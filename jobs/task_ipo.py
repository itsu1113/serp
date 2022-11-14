import click
from flask.cli import with_appcontext
from common.common import *
from logger import logger
driver=get_driver()
@click.command('task_ipo', help="Hello World.") 
@with_appcontext
def task_ipo_run():
    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_ipo'+process_date+'.tsv'

    driver.get("https://ipokabu.net/yotei/")
    today = datetime.date.today()

    for month_info in driver.find_elements(By.CLASS_NAME, 'nosp'):
        month_info_index=0
        for kigyo in month_info.find_elements(By.CLASS_NAME, 'td_ipo_soneki'):
            # 企業名
            kigyo_mei=month_info.find_elements(By.CLASS_NAME, 'td_kigyo')[month_info_index].find_element(By.TAG_NAME, "a").get_attribute('innerHTML')

            # 主幹事
            ipo_syu=month_info.find_elements(By.CLASS_NAME, 'ipo_syu')[month_info_index].find_element(By.TAG_NAME, "a").get_attribute('innerHTML')

            # 予想利益
            ipo_soneki=kigyo.get_attribute('innerHTML').replace( '\n' , '' ).replace( ' ' , '' )
            
            # ブックビルディング
            ipo_yotei2   =get_yotei(month_info, month_info_index)
            end_str      =ipo_yotei2.split('～')[1]
            end_month_day=end_str[0:end_str.find(' ')].split('/')
            end_date     =datetime.date(today.year, int(end_month_day[0]), int(end_month_day[1]))
            entry_date   =get_entry_date(end_date)
            lottery_date =get_lottery_date(entry_date)
            
            if is_exclude_syu(ipo_syu):
                continue
            
            # 結果出力　日付	""	タイトル	説明
            # print(entry_date.strftime('%Y/%m/%d')+"\t"+"\t"+"IPO"+"\t"+kigyo_mei+","+ipo_syu+","+ipo_soneki)
            request_date=[]
            request_date.append(entry_date.strftime('%Y/%m/%d'))
            request_date.append("")
            request_date.append("IPO")
            request_date.append(kigyo_mei+","+ipo_syu+","+ipo_soneki)
            
            # 抽選日を出力
            # print(lottery_date.strftime('%Y/%m/%d')+"\t"+"\t"+"抽選"+"\t"+kigyo_mei+","+ipo_syu)
            result_date=[]
            result_date.append(lottery_date.strftime('%Y/%m/%d'))
            result_date.append("")
            result_date.append("抽選")
            result_date.append(kigyo_mei+","+ipo_syu)

            with open("C:\\serp\\files\\"+file_name, 'a', newline="", encoding='UTF-8') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(request_date)
                writer.writerow(result_date)

            month_info_index+=1

# 除外リストに該当したらTRUE
def is_exclude_syu(ipo_syu):
    exclude_syu = ["東海東京証券", "東海東京証券","東洋証券","エイチ・エス証券"]
    return ipo_syu in exclude_syu

# ipo_yotei2かtd_ipo_syuryoから日付を取得
def get_yotei(month_info, month_info_index):
    try:
        return month_info.find_elements(By.CLASS_NAME, 'ipo_yotei2')[month_info_index].get_attribute('innerHTML')
    except:
        None
        
    try:
        return month_info.find_elements(By.CLASS_NAME, 'ipo_bosyu2')[month_info_index].get_attribute('innerHTML')
    except:
        None
        
    try:
        return month_info.find_elements(By.CLASS_NAME, 'td_ipo_syuryo')[month_info_index].get_attribute('innerHTML')
    except:
        None


