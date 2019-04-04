from os.path import dirname, join

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write, db_command, db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

import json
from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed
from zhulong.util.conf import get_conp

# driver=webdriver.Chrome()

# url="""http://jyzx.yiyang.gov.cn/jyxx/003001/003001001/2.html"""

# driver.get(url)


_name_='huainan'

def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]
    if cc_text != c_text:

        driver.find_element_by_xpath('//div[@class="ewb-location"]/a[4]').click()
        locator = (By.XPATH, '//div[@class="ewb-info-hd"][{}]/a[2]'.format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        locator = (By.XPATH, '//div[@class="pagemargin"]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum = re.findall('(\d+)/', cnum)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//li[@class="ewb-info-item"][1]/a').text
        # print(val)
        driver.execute_script("window.location.href='./?Paging={}'".format(num))

        locator = (By.XPATH, '//li[@class="ewb-info-item"][1]/a')
        WebDriverWait(driver, 10).until_not(EC.text_to_be_present_in_element(locator, val))

def f1(driver, num):
    locator = (By.XPATH, '//li[@class="ewb-info-item"][1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('//div[@class="ewb-location"]/span').text.strip()

    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            # 增量更新
            if num > CDC_NUM: return

            chang_address(driver, i, c_text)
            chang_page(driver, num)
            is_useful = True
            break

    if 'is_useful' not in locals():
        print('页数不合法%d' % num)
        return

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find_all('li', class_='ewb-info-item')

    for tr in lis:

        href = tr.a['href']
        name = tr.a['title']
        ggstart_time = tr.span.get_text()
        if 'http' in href:
            href = href
        else:
            href = 'http://www.hnsztb.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df = pd.DataFrame(data=data)

    df["info"] = None
    return df


def f2(driver):
    global PAGE
    global CC_TEXT
    PAGE = []
    CC_TEXT = []
    locator = (By.XPATH, '//li[@class="ewb-info-item"][1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = 0
    url=driver.current_url
    if '002001005002' in url:
        j = 2
    else:
        j=4

    for i in range(1, j):
        if i != 1:
            driver.find_element_by_xpath('//div[@class="ewb-location"]/a[4]').click()
            locator = (By.XPATH, '//div[@class="ewb-info-hd"][{}]/a[2]'.format(i))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            locator = (By.XPATH, '//div[@class="pagemargin"]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        try:
            total_ = driver.find_element_by_xpath('//td[@class="huifont"]').text
            total_ = re.findall('/(\d+)', total_)[0]
        except:
            total_ = 0

        c_text = driver.find_element_by_xpath('//div[@class="ewb-location"]/span').text.strip()
        total_ = int(total_)
        PAGE.append(total_)
        CC_TEXT.append(c_text)
        total = total + int(total_)

    total = int(total)
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '/html/body/div[3]/div[2]/div/div/div/table | /html/body/div[3]/div[2]/div/div[1] | //div[@class="ewb-info"]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    div=soup.find('div',id="mainContent")
    if div == None:
        div = soup.find('div', attrs={'id': re.compile('menutab_5_\d'), 'style': ''})
        if div == None:
            div=soup.find('div', attrs={'id': re.compile('menutab_4_\d'), 'style': ''})

    return div


data = [
    ["gcjs_zhaobiao_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001001/002001001001/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["gcjs_dayibiangeng_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001003/002001003002/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001004/002001004003/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001002/002001002001/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ######小额项目
    ["gcjs_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001005/002001005002/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002001/002002001001/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_dayibiangeng_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002005/002002005001/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_dyxly_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002006/002002006001/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiao_gg", "http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002002/002002002001/?Paging=1",["name", "ggstart_time", "href", "info"], f1, f2],

    ]




if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000

def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省淮南市",**args)
    est_html(conp,f=f3,**args)


# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None



if __name__=='__main__':

    work(conp=["postgres", "since2015", "192.168.3.171", "anhui", "huainan"],cdc_total=None)

