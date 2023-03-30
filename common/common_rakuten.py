from common.common import *

# 売り切れかどうか
def is_sold(driver):
    try:
        if driver.find_element(By.XPATH,'//*[@id="floatingCartWidget"]/div/span[4]/a/span').get_attribute("innerHTML")=='売り切れ':
            return True
        else:
            return False
    except Exception as e:
            return False


# 基本倍率を取得_楽天
def get_basic_point(driver):
    try:
        point=driver.find_element(By.CSS_SELECTOR, "#rakutenLimitedId_cart > tbody > tr:nth-child(2) > td > div > div > ul.point-summary__campaign___2KiT-.point-summary__multiplier-up___3664l.point-up > li:nth-child(2)").get_attribute('innerHTML')
        point=point.replace("倍UP", "")
        return int(point)
    except Exception as e:
        try:
            point=driver.find_element(By.CSS_SELECTOR, "#rakutenLimitedId_cart > tbody > tr:nth-child(3) > td > div > div > ul.point-summary__campaign___2KiT-.point-summary__multiplier-up___3664l.point-up > li:nth-child(2)").get_attribute('innerHTML')
            point=point.replace("倍UP", "")
            return int(point)
        except Exception as e:
            #楽天ブックス
            try:
                point=driver.find_element(By.CSS_SELECTOR, "#productInfo > div.productInfoArea > div.bdg-point-display > div > ul.point-summary__campaign___2KiT-.point-summary__multiplier-up___3664l > li:nth-child(2)").get_attribute('innerHTML')
                point=point.replace("倍UP", "")
                return int(point)
            except Exception as e:
                #楽天ブックス
                try:
                    point=driver.find_element(By.CSS_SELECTOR, "#productInfo > div.productInfoArea > div > div > ul.point-summary__campaign___2KiT-.point-summary__multiplier-up___3664l > li:nth-child(2)").get_attribute('innerHTML')
                    point=point.replace("倍UP", "")
                    return int(point)
                except Exception as e:
                    try:
                        point=driver.find_element(By.CSS_SELECTOR, "#rakutenLimitedId_cart > tbody > tr:nth-child(3) > td > div > div > ul.point-summary__campaign___2KiT-.point-summary__rebate___OwnwU.point-superdeal > li:nth-child(2)").get_attribute('innerHTML')
                        point=point.replace("%ポイントバック", "")
                        point=int(point)-1
                        return point
                    except Exception as e:
                        try:
                            point=driver.find_element(By.CSS_SELECTOR, "#rakutenLimitedId_cart > tbody > tr:nth-child(2) > td > div > div > ul.point-summary__campaign___2KiT-.point-summary__rebate___OwnwU.point-superdeal > li:nth-child(2)").get_attribute('innerHTML')
                            point=point.replace("%ポイントバック", "")
                            point=int(point)-1
                            return point
                        except Exception as e:
                            #楽天ビック
                            try:
                                point=driver.find_element(By.CSS_SELECTOR, "#item > div > div.p-productDetailv2__mainRight > div:nth-child(6) > div > div > div > ul.point-summary__campaign___2KiT-.point-summary__rebate___OwnwU > li:nth-child(2)").get_attribute('innerHTML')
                                point=point.replace("%ポイントバック", "")
                                point=int(point)-1
                                return point
                            except Exception as e:
                                #楽天ビック
                                try:
                                    point=driver.find_element(By.CSS_SELECTOR, "#item > div > div.p-productDetailv2__mainRight > div:nth-child(7) > div > div > div > ul.point-summary__campaign___2KiT-.point-summary__rebate___OwnwU > li:nth-child(2)").get_attribute('innerHTML')
                                    point=point.replace("%ポイントバック", "")
                                    point=int(point)-1
                                    return point
                                except Exception as e:
                                    #楽天ビック
                                    try:
                                        point=driver.find_element(By.CSS_SELECTOR, "#item > div > div.p-productDetailv2__mainRight > div:nth-child(8) > div > div > div > ul.point-summary__campaign___2KiT-.point-summary__multiplier-up___3664l > li:nth-child(2)").get_attribute('innerHTML')
                                        point=point.replace("倍UP", "")
                                        return int(point)
                                    except Exception as e:
                                        return 0


# 価格を取得_楽天
def get_price(driver):
    try:
        return int(driver.find_element(By.ID, "priceCalculationConfig").get_attribute("data-price"))
    except Exception as e:
        #楽天ビック
        try:
            return int(driver.find_element(By.CLASS_NAME, "p-productDetailv2__priceValue").text.replace("円(税込)", "").replace(",", ""))
        except Exception as e:
            #楽天ブックス
            try:
                price = driver.find_element(By.CSS_SELECTOR, "#productInfo > div.productInfoArea > p > span.price").get_attribute("content")
                price = int(price)
                return price
            except Exception as e:
                #楽天ブックス
                try:
                    price = driver.find_element(By.CSS_SELECTOR, "#productInfo > div.productInfoArea > p > span:nth-child(6)").get_attribute("content")
                    price = int(price)
                    return price
                except Exception as e:
                    #楽天ブックス
                    try:
                        price = int(driver.find_element(By.ID, "priceCalculationConfig").get_attribute("data-price"))
                        return price
                    except Exception as e:
                        return '-'

# jan_codeを取得_楽天
def get_jan_code(driver):
    try:
        normal_reserve_item_name = driver.find_element(By.CLASS_NAME, 'normal_reserve_item_name') 
        jan_code=normal_reserve_item_name.find_element(By.XPATH, "//meta[@itemprop='gtin13']").get_attribute('content')
        return jan_code
    except Exception as e:
        try:
            # 楽JAN
            jan_code = driver.find_element(By.ID, "rakujan-wrapper").get_attribute('data-rakujan-jan')
            return jan_code
        except Exception as e:
            # print(driver.current_url)
            raise e

