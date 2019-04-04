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
# url="http://www.szggzyjy.cn/szfront/jyxx/002001/002001001/002001001001/"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_='luan'

def chang_address(driver,i,c_text,c_type):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[2]').click()
        locator = (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[1]/div/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('//li[@class="wb-tree-items haschild"][{}]'.format(i)).click()
        time.sleep(0.1)
        driver.find_element_by_xpath(
            '//li[@class="wb-tree-items haschild current"]/ul/li/a[contains(string(),"{c_type}")]'.format(
                c_type=c_type)).click()

        locator = (By.XPATH, '//font[@class="currentpostionfont01"]/../font[2]/a[4]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    try:
        driver.switch_to.frame(1)
        mark=1
    except:
        mark=0
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]
    url=driver.current_url
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//li[@class="ewb-plate-list clearfix"]/a').text

        if mark:
            mark_1 = url.strip('/').rsplit('/', maxsplit=1)[1]
            driver.execute_script("window.location.href='./morezbgg.aspx?CategoryNum={}&Paging={}'".format(mark_1, num))
        else:
            driver.execute_script("window.location.href='./?Paging={}'".format(num))

        locator = (By.XPATH, '//li[@class="ewb-plate-list clearfix"]/a[not(contains(string(),"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):

    #PAGE中包含各个类型页面的总页数

    try:
        driver.switch_to.frame(1)
        mark=1
    except:
        mark=0
    # 第一个等待
    locator = (By.XPATH, '//li[@class="ewb-plate-list clearfix"]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    if mark:
        driver.switch_to.parent_frame()

    c_type = driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[4]').text.strip()
    c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[3]').text.strip()

    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            # 增量更新
            if num > CDC_NUM : return
            # if num > 5 : return

            chang_address(driver, i, c_text,c_type)
            chang_page(driver, num)
            is_useful = True
            break

    if 'is_useful' not in locals():
        print('页数不合法%d' % num)
        return

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('li', class_="ewb-plate-list clearfix")

    for tr in trs:
        href = tr.a['href']
        name = tr.a['title']

        ggstart_time = tr.span.get_text()
        if 'http' in href:
            href = href
        else:
            href = 'http://www.laztb.gov.cn' + href

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
    try:
        driver.switch_to.frame(1)
        mark=1
    except:
        mark=0
    # 第一个等待
    locator = (By.XPATH, '//li[@class="ewb-plate-list clearfix"]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    if mark:
        driver.switch_to.parent_frame()

    c_type = driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[4]').text.strip()
    c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[3]').text.strip()

    driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[2]').click()
    locator = (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find_all('li', class_='wb-tree-items haschild')

    total = 0
    for i in range(1, len(lis)+1):

        driver.find_element_by_xpath('//li[@class="wb-tree-items haschild"][{}]'.format(i)).click()
        time.sleep(0.1)
        try:
            driver.find_element_by_xpath(
            '//li[@class="wb-tree-items haschild current"]/ul/li/a[contains(string(),"{c_type}")]'.format(
                c_type=c_type)).click()
            locator = (By.XPATH, '//font[@class="currentpostionfont01"]/../font[2]/a[4]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            content=driver.find_element_by_xpath('//li[@class="wb-tree-items haschild current"]/ul').text
            if c_type in content:
                raise TimeoutError
            else:
                continue

        try:
            driver.switch_to.frame(1)
            mark=1
        except:
            mark=0

        try:
            page = driver.find_element_by_xpath('//td[@class="huifont"]').text
            total_ = re.findall(r'/(\d+)', page)[0]
        except:
            total_=0
        if mark:
            driver.switch_to.parent_frame()

        c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[3]').text.strip()


        total_=int(total_)
        PAGE.append(total_)
        CC_TEXT.append(c_text)
        total = total + int(total_)

        driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[2]').click()
        locator = (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[1]/div/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total=int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@data-role="tab-content" and not(@class)]/div/table | //div[@class="ewb-detail-info"]')

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
    try:
        div = soup.find('div', attrs={'data-role': "tab-content", 'class': ''})
        table = div.find('table')
        div = table.find('td', class_='infodetail')
    except:
        div = soup.find('div', class_="ewb-detail-info")

        if div == None:
            raise ValueError

    return div




data=[
    ["gcjs_zhaobiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002001/002001001/002001001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_biangen_gg","http://www.laztb.gov.cn/laztb/jyxx/002001/002001001/002001001002/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.laztb.gov.cn/laztb/jyxx/002001/002001001/002001001003/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002001/002001001/002001001004/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002002/002002001/002002001001/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_biangen_gg","http://www.laztb.gov.cn/laztb/jyxx/002002/002002001/002002001002/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002002/002002001/002002001003/",["name","ggstart_time","href","info"],f1,f2],

    ["qsy_qita_zhaobiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002005/002005001/002005001001/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_qita_biangen_gg","http://www.laztb.gov.cn/laztb/jyxx/002005/002005001/002005001002/",["name","ggstart_time","href","info"],f1,f2],
    ##包含流标中标
    ["qsy_qita_gg","http://www.laztb.gov.cn/laztb/jyxx/002005/002005001/002005001003/",["name","ggstart_time","href","info"],f1,f2],
    ##只有市本级有少量数据，未爬取
    #####["qsy_qita_jieguo_gg","http://www.laztb.gov.cn/laztb/jyxx/002005/002005001/002005001004/",["name","ggstart_time","href","info"],f1,f2],

    ["qsy_xiane_zhaobiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002006/002006001/002006001001/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_xiane_biangen_gg","http://www.laztb.gov.cn/laztb/jyxx/002006/002006001/002006001002/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_xiane_gg","http://www.laztb.gov.cn/laztb/jyxx/002006/002006001/002006001003/",["name","ggstart_time","href","info"],f1,f2],
    ##包含中标，流标
    ["qsy_xianqu_zhaobiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002007/002007001/002007001001/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_xianqu_biangen_gg","http://www.laztb.gov.cn/laztb/jyxx/002007/002007001/002007001002/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_xianqu_zhongbiao_gg","http://www.laztb.gov.cn/laztb/jyxx/002007/002007001/002007001003/",["name","ggstart_time","href","info"],f1,f2],

]




if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000


def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省六安市",**args)
    est_html(conp,f=f3,**args)

# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None


if __name__=='__main__':

    work(conp=["postgres", "since2015", "192.168.3.171", "anhui", "luan"],cdc_total=None)

