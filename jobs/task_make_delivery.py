from common.common_rakuten import *
# webdriver
driver=get_driver()
@click.command('task_make_delivery', help="Hello World.") 
@with_appcontext
def task_make_delivery_run():
    try:
        input_list=[]
        f = open("C:\\serp\\files\\input\\1col.tsv", 'r', encoding='UTF-8')
        for data in f:
            input_list.append(data.rstrip('\n'))
        f.close()

        for asin in input_list:
            
            search_box=driver.find_element(By.ID, "myitable-search")
            search_box.clear()
            search_box.send_keys(asin)
            # focusToElement(driver, By.CSS_SELECTOR, "#myitable-search-button > span > input", True)
            driver.find_element(By.CSS_SELECTOR, "#myitable-search-button > span > input").click()
            time.sleep(2)
            driver.find_element(By.ID, "mt-select-all").click()
            hit_count=driver.find_element(By.ID, "mt-header-count-value").get_attribute('innerHTML')
            if hit_count!='1':
                print(asin)

    except Exception as e:
        print(e)
