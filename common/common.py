import click
from flask.cli import with_appcontext
from logger import logger
from time import sleep
from bs4 import BeautifulSoup
import requests
import webbrowser
from os.path import join
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
import os
import io
import sys
import csv
import ast
import datetime
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from sp_api.api import Catalog
from sp_api.api import ProductFees
from sp_api.base.marketplaces import Marketplaces
import sys
import hashlib
import hmac
import datetime
import re
import requests
import json
import time
import urllib.request
import urllib.parse
import pprint
from selenium import webdriver
import keepa
from settings import *
from datetime import timedelta
import jpholiday

def get_driver():
    driver_path="C:\\Users\\ItsukiSato\\Documents\\20_TOOL\\chromedriver.exe"
    # 起動時にオプションをつける。（ポート指定により、起動済みのブラウザのドライバーを取得）
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    return driver
    
def close_tab(driver):
    try:
        # タブが一つになるまで開いているタブを閉じる
        for x in range(1, len(driver.window_handles)):
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
    except Exception as e:
        print('Exception:'+'close_tab')
        print(e)

# アマゾン出品許可チェック
def chek_approved(driver, result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue

            result['leafer_url'] = 'https://leafer.jp/Search?code='+result['asin']
            
            amazon_url='https://www.amazon.co.jp/dp/'+result['asin']+'/ref=olp_aod_redir_impl1?_encoding=UTF8&aod=1'
            result['amazon_url'] = amazon_url

            seller_url='https://sellercentral.amazon.co.jp/abis/listing/syh?asin='+result['asin']+'&ref_=xx_catadd_dnav_xx#offer'
            result['seller_url'] = seller_url
            
            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(seller_url)
            time.sleep(3)#3秒必要
            
            if driver.title == 'Server Busy':
                logger.debug('Server Busy '+ result['asin'])
                driver.quit()

            # 出品できるか　できない場合はexception
            check=driver.find_element(By.ID,'reconcile-item-title').get_attribute("innerHTML")
            result['approved'] = '○'
            
            # 新品出品OKか
            condition=driver.find_element(By.XPATH,'//*[@id="condition_type"]').get_attribute("options")
            condition=ast.literal_eval(condition)
            wk_condition='-'
            for c in condition:
                if c['name']=='新品':
                    wk_condition='○'
                    break
            result['condition'] = wk_condition
            if wk_condition == '-':
                result['invalid']=1

        except NoSuchElementException as e:
            result['approved']  = '-'
            result['condition'] = '-'
            result['invalid']=1
            continue
        except Exception as e:
            result['approved']  = '？'
            result['condition'] = '？'
            result['invalid']=1
            print(e)
            continue

# リーファ販売数量チェック
def chek_sales(driver, result_list):
    for result in result_list:
        try:
            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(result['leafer_url'])
            time.sleep(3)
            
            # 3ヶ月合計販売数量
            sales_volume=driver.find_element(By.XPATH,'//*[@id="MainContent_lbl_NewSum"]').get_attribute("innerHTML")
            result['sales_volume'] = '-' if int(sales_volume)<=5 else '○'
            
        except NoSuchElementException as e:
            result['sales_volume'] = 'e'
            print(e)
            continue
        except Exception as e:
            result['sales_volume'] = 'e'
            print(e)
            continue

def check_restrict():
    try:
        restrict=driver.find_element(By.ID, 'MainContent_lbl_Message').get_attribute("innerHTML")
        if restrict=='一定期間に大量のアクセスがあったため、一時アクセスが制限されています。':
            return True
        else:
            return False
    except Exception as e:
        return False

def get_leafer(driver, result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue
            leafer_url='https://leafer.jp/Search?code='+result['jan_code']
            result['leafer_url']=leafer_url
            keepa_url='https://keepa.com/#!search/5-'+result['jan_code']
            result['keepa_url']=keepa_url
            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(leafer_url)
            time.sleep(0.5)
            
            # アクセス制限チェック
            if check_restrict():
                logger.debug('restrict')
                break
            
            # asinを取得
            asin=driver.find_element(By.ID, "MainContent_lbl_Asin").get_attribute('value')
            result['asin']=asin
            # 商品名
            shohin_name=driver.find_element(By.ID, "MainContent_lbl_Title").get_attribute('innerHTML')
            result['shohin_name']=shohin_name
            # 出品価格
            cart=driver.find_element(By.ID, "MainContent_txt_SalesPlanPrice").get_attribute('value')
            result['cart']=cart
            # 出品者数
            seller_num=driver.find_element(By.ID, "MainContent_lbl_NewSeller").get_attribute('innerHTML')
            result['seller_num']=seller_num
            # if int(seller_num)==1: 
            #     result['invalid']=1
            # 3ヶ月合計販売数量
            sales_volume = driver.find_element(By.XPATH, '//*[@id="MainContent_lbl_NewSum"]').get_attribute("innerHTML")
            result['sales_volume']=int(sales_volume)
            # 損益分岐点
            bunkiten=driver.find_element(By.ID, "MainContent_lbl_NewDeposit").get_attribute('innerHTML')
            bunkiten=str(bunkiten).replace('￥', '')
            result['bunkiten']=bunkiten

        except NoSuchElementException as e:
            result['invalid']=1
            # print(e)
            continue
        except Exception as e:
            result['invalid']=1
            print(e)
            continue

def get_leafer_asin(driver, result_list):
    for result in result_list:
        try:
            # 無効なレコードはスキップ
            if result['invalid']==1:
                continue
            leafer_url='https://leafer.jp/Search?code='+result['asin']
            result['leafer_url']=leafer_url
            keepa_url='https://keepa.com/#!product/5-'+result['asin']
            result['keepa_url']=keepa_url
            # URLを開く
            driver.switch_to.window(driver.window_handles[0])
            driver.get(leafer_url)
            time.sleep(0.5)
            
            # アクセス制限チェック
            if check_restrict():
                logger.debug('restrict')
                break
            
            # jan_codeを取得
            jan_code=driver.find_element(By.ID, "MainContent_lbl_Jan").get_attribute('value')
            result['jan_code']=jan_code
            # 商品名
            shohin_name=driver.find_element(By.ID, "MainContent_lbl_Title").get_attribute('innerHTML')
            result['shohin_name']=shohin_name
            # 出品価格
            cart=driver.find_element(By.ID, "MainContent_txt_SalesPlanPrice").get_attribute('value')
            result['cart']=cart
            # 出品者数
            seller_num=driver.find_element(By.ID, "MainContent_lbl_NewSeller").get_attribute('innerHTML')
            result['seller_num']=seller_num
            # if int(seller_num)==1: 
            #     result['invalid']=1
            # 3ヶ月合計販売数量
            sales_volume = driver.find_element(By.XPATH, '//*[@id="MainContent_lbl_NewSum"]').get_attribute("innerHTML")
            result['sales_volume']=int(sales_volume)
            # 損益分岐点
            bunkiten=driver.find_element(By.ID, "MainContent_lbl_NewDeposit").get_attribute('innerHTML')
            bunkiten=str(bunkiten).replace('￥', '')
            result['bunkiten']=bunkiten
        except NoSuchElementException as e:
            result['invalid']=1
            print(e)
            continue
        except Exception as e:
            result['invalid']=1
            print(e)
            continue


# リクエストヘッダーを作成
def make_get_authorization_header(method, canonical_uri, request_parameters, token):

    # ************* REQUEST VALUES *************
    service = 'execute-api'
    host = 'sellingpartnerapi-fe.amazon.com'
    region = 'us-west-2'
    user_agent = "My Selling Tool/2.0 (Language=Java/1.8.0.221; Platform=Windows/10)"

    access_key = ''
    secret_key = ''

    # Key derivation functions. See:
    # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python

    def sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = sign(kDate, regionName)
        kService = sign(kRegion, serviceName)
        kSigning = sign(kService, 'aws4_request')
        return kSigning

    # Read AWS access key from env. variables or configuration file. Best practice is NOT
    # to embed credentials in code.
    if access_key is None or secret_key is None:
        raise Exception('No access key is available.')

    # Create a date for headers and the credential string
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    # Date w/o time, used in credential scope
    datestamp = t.strftime('%Y%m%d')

    # ************* TASK 1: CREATE A CANONICAL REQUEST *************
    # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
    canonical_querystring = request_parameters
    canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'

    signed_headers = 'host;x-amz-date'

    payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()

    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + \
        '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    # ************* TASK 2:     *************
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + \
        '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' + amzdate + '\n' + credential_scope + \
        '\n' + \
        hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    # ************* TASK 3: CALCULATE THE SIGNATURE *************
    signing_key = getSignatureKey(secret_key, datestamp, region, service)

    # Sign the string_to_sign using the signing_key
    signature = hmac.new(signing_key, (string_to_sign).encode(
        'utf-8'), hashlib.sha256).hexdigest()

    # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + \
        credential_scope + ', ' + 'SignedHeaders=' + \
        signed_headers + ', ' + 'Signature=' + signature

    # x-amz-date はPostmanでは自動で付与してくれるので設定してませんが必要です
    headers = {'x-amz-access-token': token, 'user-agent': user_agent,
               'x-amz-date': amzdate, 'Authorization': authorization_header}

    return headers

# APIを呼び出す
def apicall_sp_api_get(canonical_uri, headers, request_parameters) -> dict:

    # リクエストデータを作成
    endpoint = 'https://sellingpartnerapi-fe.amazon.com' + canonical_uri
    request_url = endpoint + '?' + request_parameters

    # リクエストを送信
    response = requests.get(request_url, headers=headers)

    result_dict = json.loads(response.text)

    return result_dict


# アクセストークンを生成する
def get_access_token():
    url_items = 'https://api.amazon.com/auth/o2/token'
    item_data = {
        'grant_type': '',
        'refresh_token': '',
        'client_id': '',
        'client_secret': ''
    }
    r_post = requests.post(url_items, headers='', json=item_data)
    access_token = r_post.json()['access_token']
    
    return access_token

# ASIN、商品名を取得
def get_catalog(jan_code):
    try:
        ret=dict()
        method = 'GET'
        canonical_uri = '/catalog/v0/items'
        # アクセストークンを発行
        access_token=get_access_token()

        # 並び順はkeyのアルファベット順ではないとエラーになるようです。
        #　ここでは下でsortedしていていますが注意が必要です
        request_parameters_unencode = {
            'MarketplaceId': '',
            'JAN': jan_code
        }
        request_parameters = urllib.parse.urlencode(sorted(request_parameters_unencode.items()))

        # AWS 認証情報を作成
        headers = make_get_authorization_header(method, canonical_uri, request_parameters, access_token)
        # リクエスト発行
        response = apicall_sp_api_get(canonical_uri, headers, request_parameters)

        ret['Title']=response['payload']['Items'][0]['AttributeSets'][0]['Title']
        ret['ASIN']=response['payload']['Items'][0]['Identifiers']['MarketplaceASIN']['ASIN']
        return ret
    except Exception as e:
        print(e)
        ret['Title']=''
        ret['ASIN']=''
        return ret
        

# 新品最安値を取得する
def get_price(asin):
    try:
        method = 'GET'
        canonical_uri = '/products/pricing/v0/items/'+asin+'/offers'
        # アクセストークンを発行
        access_token=get_access_token()

        # 並び順はkeyのアルファベット順ではないとエラーになるようです。
        #　ここでは下でsortedしていていますが注意が必要です
        request_parameters_unencode = {
            'MarketplaceId': '',
            'ItemCondition': 'New',
            'Asin': asin
        }
        request_parameters = urllib.parse.urlencode(sorted(request_parameters_unencode.items()))

        # AWS 認証情報を作成
        headers = make_get_authorization_header(method, canonical_uri, request_parameters, access_token)

        # リクエスト発行
        response = apicall_sp_api_get(canonical_uri, headers, request_parameters)
        LowestPrices=response['payload']['Summary']['LowestPrices']
        lowest_price=0
        for l in LowestPrices:
            if l['condition']=='new':
                if lowest_price==0:
                    lowest_price=l['LandedPrice']['Amount']
                else:
                    if lowest_price>l['LandedPrice']['Amount']:
                        lowest_price=l['LandedPrice']['Amount']

        return lowest_price
    except Exception as e:
        return 0

# 販売手数料を取得
def fee_estimator_asin(ASIN,productPrice,currencyCode,shippingPrice,FBA):
    # 商品手数料オブジェクト
    productfees = ProductFees(marketplace=Marketplaces.JP,   # 対象のマーケットプレイスを指定
                  credentials=credentials)                   # API情報を指定
    # 結果取得
    result = productfees.get_product_fees_estimate_for_asin(asin=ASIN,
                                                            price=productPrice,
                                                            currency=currencyCode,
                                                            shipping_price=shippingPrice, 
                                                            is_fba=FBA,
                                                            )
    return result


# [販売手数料＋FBA手数料]を取得
def get_fee(asin):
    try:
        asin           = asin
        currencyCode   = 'JPY'           # 通貨コード
        productPrice   = get_price(asin)            # 商品販売価格
        shippingPrice  = 0             # 発送手数料
        FBA            = True            # FBA利用：True, FBA利用なし：False

        credentials=dict(
                    refresh_token     = '',   # Amazon Seller開発者登録後に入手可能
                    lwa_app_id        = '',        # Amazon Seller開発者登録後に入手可能
                    lwa_client_secret = '',   # Amazon Seller開発者登録後に入手可能
                    aws_access_key    = '',      #（AWS IAMユーザーロール登録時に取得可能）
                    aws_secret_key    = '',  #（AWS IAMユーザーロール登録時に取得可能）
                    role_arn          = '',        #（AWS IAMユーザーロール登録時に取得可能）
                    )

        # 商品手数料オブジェクト
        productfees = ProductFees(marketplace=Marketplaces.JP,   # 対象のマーケットプレイスを指定
                      credentials=credentials)                   # API情報を指定
        # 結果取得
        result = productfees.get_product_fees_estimate_for_asin(asin=asin,
                                                                price=productPrice,
                                                                currency=currencyCode,
                                                                shipping_price=shippingPrice, 
                                                                is_fba=FBA,
                                                                )()
        
        
        return int(result['FeesEstimateResult']['FeesEstimate']['TotalFeesEstimate']['Amount'])
    except Exception as e:
        print(e)
        return 0

# ７日後を取得
def get_lottery_date(entry_date):
    
    lottery_date=entry_date + timedelta(days=7)

    while isBizDay(lottery_date)==0:
        lottery_date+=timedelta(days=1)
    
    return lottery_date

# ２営業日前を取得
def get_entry_date(end_date):
    cnt_weekday=0
    while cnt_weekday<2:
        end_date-=timedelta(days=1)
        if isBizDay(end_date)==1:
            cnt_weekday+=1
    return end_date

# 平日の場合には1を返す
def isBizDay(DATE):
    if DATE.weekday() >= 5 or jpholiday.is_holiday(DATE):
        return 0
    else:
        return 1

