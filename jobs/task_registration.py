from common.common_rakuten import *
# webdriver
driver=get_driver()
@click.command('task_registration', help="Hello World.") 
@with_appcontext
def task_registration_run():
    try:
        input_list=[]
        f = open("C:\\serp\\files\\input\\1col.tsv", 'r', encoding='UTF-8')
        for data in f:
            input_list.append(data.rstrip('\n'))
        f.close()

        for asin in input_list:
            # 検索BOX
            search_box=driver.find_element(By.ID, "inputSeach")
            search_box.clear()
            search_box.send_keys(asin)
            # 検索ボタン
            driver.find_element(By.CSS_SELECTOR, "#content-area > div.content-wrapper > div > div > div.content-area__content > div.fba-apply > div.vx-card.fba-apply-search-bar > div.vx-card__collapsible-content.vs-con-loading__container > div > div.vx-input-group.flex.pb-6.search-group > div.vx-input-group-append.flex.w-full.justify-between > div > button").click()
            time.sleep(3)
            # 出品するボタン
            driver.find_element(By.CSS_SELECTOR, "#content-area > div.content-wrapper > div > div > div.content-area__content > div.fba-apply > div.vuedals > div > div > div.dlg-content > div:nth-child(2) > table > tbody > tr > td.td-btn > div > button > span.vs-button-text.vs-button--text").click()
            time.sleep(5)
            # 追加出品ダイアログがでているか確認
            try:
                if driver.find_element(By.CLASS_NAME, "title").get_attribute("innerHTML") == 'この商品をＦＢＡに追加納品しますか？':
                    driver.find_element(By.CSS_SELECTOR, "#content-area > div.content-wrapper > div > div > div.content-area__content > div.fba-apply > div.vuedals > div > div > div > div.dlg-content--item.text-right.mt-4 > button > span.vs-button-text.vs-button--text").click()
                    print(asin)
            except Exception as e:
                continue
        # コンディション説明をクリア
        texts = driver.find_elements(By.CLASS_NAME, "vs-textarea")
        for text in texts:
            text.clear()

    except Exception as e:
        print(e)
