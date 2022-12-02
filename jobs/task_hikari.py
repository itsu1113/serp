from common.common import *
driver=get_driver()
@click.command('task_hikari', help="Hello World.") 
@with_appcontext
def task_hikari_run():

    # 処理日
    process_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 出力ファイル名
    file_name='research_hikari'+process_date+'.tsv'
    # ランキングリスト
    cate_list=get_cate_list()
    fieldnames=[]
    is_first=True

    for category in cate_list:
        base_url="https://shop.hikaritv.net/shopping/app/catalog/list/init?searchCategoryCode="+category+"&searchWord=&searchCommodityCode=&searchMethod=0&searchType=0&squeezeSerch=0&hideKeyWord=&hidePriceMin=&hidePriceMax=&keywordToggle=&alignmentSequence=1&pageSize=50&mode=image&pageLayout=window&searchMakerName=&pointFacet=&discountRateFacet=&searchPriceStart=&searchPriceEnd=&searchTagCode=&searchCouponCode=&fqGetPoint=&fqStartDateMin=&fqStartDateMax=&fqStartDateName=&fqAverageRating=&banner=&notDisplayFacet=&currentPage="

        # p1-p5までをループする
        for i in range(1, 5):
            item_list_page=base_url+str(i)

            driver.get(item_list_page)

            shohin_list = driver.find_element(By.CLASS_NAME, "nbox_container").find_element(By.CLASS_NAME, "box2").find_elements(By.CLASS_NAME, "w50p")
            # w50pに参照できないデータがあるので精査する
            wk_shohin_list = []
            for s in shohin_list:
                try:
                    wk_shohin_list.append(s.find_element(By.TAG_NAME, "a").get_attribute("href"))
                except Exception as e:
                    next
            shohin_list = wk_shohin_list

            # wk結果リスト
            result_list = []
            for shohin in shohin_list:
                result_list.append({'invalid':0, 'category':category, 'item_url':shohin})

            # 商品情報取得
            get_item(result_list)

            # リーファ情報取得
            get_leafer(driver, result_list)

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


# カテゴリリストを定義
def get_cate_list():
    # ランキングリスト
    cate_list=list(range(0))

    cate_list.append("a0022")
    cate_list.append("a0023")
    cate_list.append("a0024")
    cate_list.append("a0025")
    cate_list.append("a0026")
    cate_list.append("a0027")
    cate_list.append("a0028")
    cate_list.append("a0030")
    cate_list.append("a0031")
    cate_list.append("a0035")
    cate_list.append("a0036")
    cate_list.append("a0038")
    return cate_list

def get_jan1():
    try:
        jan=''
        spec = driver.find_element(By.CLASS_NAME, "specTable").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        for s in spec:
            if s.find_element(By.TAG_NAME, "th").get_attribute("innerHTML") == "JANコード":
                jan = s.find_element(By.TAG_NAME, "td").get_attribute("innerHTML")
                return jan
        return jan
    except Exception as e:
        print(e)
        return '-'
    
def get_price1():
    try:
        item_price = driver.find_element(By.CLASS_NAME, "priceData").find_element(By.CLASS_NAME, "priceSet").find_element(By.CLASS_NAME, "num").get_attribute("innerHTML").replace(',', '')
        return item_price
    except Exception as e:
        return '-'
    
def get_price2():
    try:
        item_price=driver.find_element(By.CLASS_NAME, 'elPriceNumber')[0].get_attribute('innerHTML').replace(',', '').replace('円', '')
        return item_price
    except Exception as e:
        return '-'
    
def check_jan(jan):
    try:
        jan=str(jan)
        if jan.isnumeric():
            if len(jan)==13:
                return True
        return False
    except Exception as e:
        print(e)
        return False
    
def get_point():
    try:
        point = driver.find_element(By.CLASS_NAME, "pointData").find_element(By.CLASS_NAME, "priceSet").find_element(By.CLASS_NAME, "num").get_attribute("innerHTML").replace(',', '')
        return point
    except Exception as e:
        return '-'
    
def get_item(result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue

            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(result['item_url'])
            time.sleep(0.5)
            # jan
            jan=get_jan1()
            if jan=='-':
                result['invalid']=1
                continue

            # jan書式チェック
            if check_jan(jan):
                result['jan_code']=jan
            else:
                result['jan_code']=9999999999999
                result['invalid']=1
                continue

            # 獲得ポイント
            point=get_point()
            if point=='-':
                result['jan_code']=9999999999998
                result['invalid']=1
                continue

            # 仕入値
            item_price=get_price1()
            if item_price=='-':
                result['invalid']=1
                continue
            result['item_price']=int(item_price)-(int(point))

        except NoSuchElementException as e:
            result['invalid']=1
            print(e)
            continue
        except Exception as e:
            result['invalid']=1
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
            gross_profit = float(result['bunkiten']) - float(result['item_price'])
            result['gross_profit'] = gross_profit

            # 粗利率
            gross_profit_per = round(gross_profit / float(result['cart']) * 100, 1)
            result['gross_profit_per'] = gross_profit_per
                # gross_profit_per+=15 #test
            if gross_profit_per < 1:
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
