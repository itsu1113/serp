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
                            return 0


