from common.common_rakuten import *

@click.command('task_tracking', help="Hello World.") 
@with_appcontext
def task_tracking_run():
        # 処理日
        process_date = datetime.datetime.now().strftime('%Y%m%d')
        # 出力ファイル名
        file_name='research_tracking'+process_date+'.tsv'
        # webdriver
        driver=get_driver()
        input_list=[]
        f = open("C:\\serp\\files\\input\\1col.tsv", 'r', encoding='UTF-8')
        for data in f:
            input_list.append(data.rstrip('\n'))
        f.close()

        for asin in input_list:
            try:

                driver.get('https://keepa.com/#!product/5-'+asin)
                time.sleep(10)
                now_price=driver.find_element(By.XPATH, '//*[@id="productInfoBox"]/span[2]/span').get_attribute('innerHTML').replace('¥ ', '').replace(',', '')
                purpose_price=round(int(now_price)*0.75)
                driver.find_element(By.ID, "tabTrack").click()
                ama_price_element=driver.find_element(By.ID, "csvtype-5-0-threshold")
                new_price_element=driver.find_element(By.ID, "csvtype-5-1-threshold")
                ama_price_element.clear()
                new_price_element.clear()
                ama_price_element.send_keys(purpose_price)
                new_price_element.send_keys(purpose_price)
                focusToElement(driver, By.ID, "submitTracking", True)
                driver.find_element(By.ID, "submitTracking").click()
            except Exception as e:
                logger.debug('tracking error '+ asin)
                print(asin)
                print(e)
                continue

