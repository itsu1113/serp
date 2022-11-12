import click
from flask.cli import with_appcontext
from common.common import *
from logger import logger
driver=get_driver()
@click.command('task_ipo', help="Hello World.") 
@with_appcontext
def task_ipo_run():

    driver=get_driver()
    driver.get("https://ipokabu.net/yotei/")
    today = datetime.date.today()

    for month_info in driver.find_elements_by_class_name('nosp'):
        month_info_index=0
        for kigyo in month_info.find_elements_by_class_name('td_ipo_soneki'):
            # 企業名
            kigyo_mei=month_info.find_elements_by_class_name('td_kigyo')[month_info_index].find_element_by_tag_name("a").get_attribute('innerHTML')

            # 主幹事
            ipo_syu=month_info.find_elements_by_class_name('ipo_syu')[month_info_index].find_element_by_tag_name("a").get_attribute('innerHTML')

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
            print(entry_date.strftime('%Y/%m/%d')+"\t"+"\t"+"IPO"+"\t"+kigyo_mei+","+ipo_syu+","+ipo_soneki)
            
            # 抽選日を出力
            print(lottery_date.strftime('%Y/%m/%d')+"\t"+"\t"+"抽選"+"\t"+kigyo_mei+","+ipo_syu)
            
            month_info_index+=1

