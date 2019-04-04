import time
from os.path import dirname, join

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]
from zhulong.util.conf import get_conp

# url="http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001001/MoreInfo.aspx?CategoryNum=028001001001"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
_name_='maanshan'


def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]
    if cc_text != c_text:
        mark = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[2]/font').text
        if mark == '标前公示':
            driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[2]').click()
        else:
            driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[3]').click()
        locator = (By.XPATH, '(//font[@class="MoreinfoColor"])[{}]'.format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        locator = (By.XPATH, '//tr[@class="TDStylemore"][1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_link_text('更多信息').click()
        locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):

    cnum = driver.find_element_by_xpath('//div[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a').get_attribute(
            "href")[- 30:]
        # print(val)
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))

        locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):

    #PAGE中包含各个类型页面的总页数
    global PAGE
    global CC_TEXT

    locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    mark = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[2]/font').text
    if mark == '标前公示':
        c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[3]/font').text.strip()
    else:
        c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[4]/font').text.strip()

    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            # 增量更新
            if num > CDC_NUM : return

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
    div = soup.find('table', id='MoreInfoList1_DataGrid1')
    trs = div.find_all('tr', valign='top')

    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']
        ggstart_time = tds[2].get_text().strip()

        if 'http' in href:
            href = href
        else:
            href = 'http://zbcg.mas.gov.cn' + href
        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None

    driver.switch_to.parent_frame()
    return df



def f2(driver):
    global PAGE
    global CC_TEXT
    PAGE = []
    CC_TEXT = []
    total=0
    locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 第一个等待
    for i in range(1, 5):
        if i != 1:
            mark=driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[2]/font').text
            if mark =='标前公示':
                driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[2]').click()
            else:
                driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[3]').click()

            locator = (By.XPATH, '(//font[@class="MoreinfoColor"])[{}]'.format(i))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            locator = (By.XPATH, '//tr[@class="TDStylemore"][1]/td[2]/a')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_link_text('更多信息').click()
            locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            total_ = driver.find_element_by_xpath(
                '//div[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
        except:
            total_ = 0
        try:
            c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[4]/font').text.strip()
        except:
            c_text=driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[3]/font').text.strip()
        total_ = int(total_)
        PAGE.append(total_)
        CC_TEXT.append(c_text)

        total = total + int(total_)
        total = int(total)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)


    locator = (By.XPATH,
               '//*[@id="tblInfo"] | //*[@id="form1"]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table')

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

    div = soup.find('td', id="TDContent")
    if div == None:
        div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})

    return div




data=[
    ["gcjs_zhaobiao_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001001/MoreInfo.aspx?CategoryNum=028001001001",["name", "ggstart_time", "href", "info"],f1,f2],
    ["gcjs_gqita_da_bian_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001002/028001002001/MoreInfo.aspx?CategoryNum=028001002001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_zhongbiaohx_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001003/028001003001/MoreInfo.aspx?CategoryNum=028001003001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_gqita_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001005/028001005001/MoreInfo.aspx?CategoryNum=028001005001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_zhongbiao_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001006/028001006001/MoreInfo.aspx?CategoryNum=028001006001",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002001/028002001001/MoreInfo.aspx?CategoryNum=028002001001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["zfcg_gqita_da_bian_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002002/028002002001/MoreInfo.aspx?CategoryNum=028002002001",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    # 包含中标流标
    ["zfcg_gqita_zhong_liu_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002003/028002003001/MoreInfo.aspx?CategoryNum=028002003001", ["name", "ggstart_time", "href", "info"],
     f1, f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002004/028002004001/MoreInfo.aspx?CategoryNum=028002004001", ["name", "ggstart_time", "href", "info"],
     f1, f2],

    ["qsy_yucai_gg", "http://zbcg.mas.gov.cn/maszbw/jygg/028007/028007001/MoreInfo.aspx?CategoryNum=028007001", ["name", "ggstart_time", "href", "info"], f1, f2],

]





if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 10
else:
    CDC_NUM = 10000


def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省马鞍山市",**args)
    est_html(conp,f=f3,**args)

# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None


if __name__=='__main__':

    work(conp=["postgres","since2015","192.168.3.171","anhui","maanshan"])
    pass