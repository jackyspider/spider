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
# url="http://www.szggzyjy.cn/szfront/jyxx/002002/002002001/002002001001/"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)




_name_='suzhou'

def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=driver.find_element_by_xpath(
        '//td[@class="LeftMenuSubBg" and not(@style)]/table/tbody/tr/td[not(@style or @class)]/table/tbody/tr[{}]/td/a/font'.format(i)).text
    cc_text=re.findall(r'【(.+)】',cc_text)[0]

    if cc_text != c_text:
        try:
            val = driver.find_element_by_xpath('//ul[@class="ewb-lbd-items"]/li/a').text
        except:
            val='none'
        driver.find_element_by_xpath(
            '//td[@class="LeftMenuSubBg" and not(@style)]/table/tbody/tr/td[not(@style or @class)]/table/tbody/tr[{}]/td/a'.format(i)).click()

        locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))



def chang_page(driver,num):


    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]

    #第一页不用翻页
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//ul[@class="ewb-lbd-items"]/li/a').get_attribute(
            "href").rsplit('/',maxsplit=1)[1]

        #翻页
        driver.execute_script("window.location.href='./?Paging={}'".format(num))

        locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def f1(driver,num):

    #PAGE中包含各个类型页面的总页数

    try:
        locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        locator = (By.XPATH, '//div[@class="ewb-list-bd"]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/span').text


    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            #增量更新
            if num > CDC_NUM :return

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
    div = soup.find('ul', class_='ewb-lbd-items')
    trs = div.find_all('li')
    # print(len(trs))
    for tr in trs:
        href = tr.a['href']
        name = tr.a['title']
        ggstart_time = tr.span.get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.szggzyjy.cn' + href


        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)

    df["info"] = None
    return df




def f2(driver):
    global PAGE

    PAGE=[]

    try:
        locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        time.sleep(1)

    total = 0
    for i in range(1, 7):
        if i != 1:
            try:
                val = driver.find_element_by_xpath('//ul[@class="ewb-lbd-items"]/li/a').get_attribute(
            "href").rsplit('/',maxsplit=1)[1]
            except:
                val='kong'
            driver.find_element_by_xpath(
                '//td[@class="LeftMenuSubBg" and not(@style)]/table/tbody/tr/td[not(@style or @class)]/table/tbody/tr[{}]/td/a'.format(
                    i)).click()
            locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a[not(contains(@href,"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        try:
            page = driver.find_element_by_xpath('//td[@class="huifont"]').text

            total_ = re.findall(r'/(\d+)', page)[0]
        except:
            total_ = 0
        total_=int(total_)
        PAGE.append(total_)

        total = total + int(total_)
    total = int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, '/html/body')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    if '页面有误' in html:
        return '404'

    locator = (By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2] | //div[@class="ewb-list-bd"] | //div[@class="ewb-mt6"]')
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

    div = soup.find('div', id='mainContent')

    if div == None:
        div = soup.find('div', attrs={'id': re.compile('menutab_5_\d'), 'style': ''})
        if div == None:
            div = soup.find('div', attrs={'id': re.compile('menutab_4_\d'), 'style': ''})
            if div == None:
                raise ValueError
    return div

def f4(driver,num):
    locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    chang_page(driver,num)

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('ul', class_='ewb-lbd-items')
    trs = div.find_all('li')
    # print(len(trs))
    for tr in trs:
        href = tr.a['href']
        name = tr.a['title']
        ggstart_time = tr.span.get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.szggzyjy.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df
def f5(driver):
    locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text

        total = re.findall(r'/(\d+)', page)[0]
    except:
        total = 0

    total = int(total)
    driver.quit()

    return total


data=[
    ["gcjs_zhaobiao_gg","http://www.szggzyjy.cn/szfront/jyxx/002001/002001001/002001001001/",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_gqita_da_bian_gg","http://www.szggzyjy.cn/szfront/jyxx/002001/002001002/002001002001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.szggzyjy.cn/szfront/jyxx/002001/002001003/002001003001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.szggzyjy.cn/szfront/jyxx/002001/002001004/002001004001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_liubiao_gg","http://www.szggzyjy.cn/szfront/jyxx/002001/002001006/002001006001/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_yvcai_gg","http://www.szggzyjy.cn/szfront/jyxx/002002/002002001/002002001001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiao_gg","http://www.szggzyjy.cn/szfront/jyxx/002002/002002002/002002002001/",["name","ggstart_time","href","info"],f1,f2],
    #包含答疑和变更
    ["zfcg_gqita_da_bian_gg","http://www.szggzyjy.cn/szfront/jyxx/002002/002002003/002002003001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.szggzyjy.cn/szfront/jyxx/002002/002002004/002002004001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_liubiao_gg","http://www.szggzyjy.cn/szfront/jyxx/002002/002002006/002002006001/",["name","ggstart_time","href","info"],f1,f2],

    ["qsy_zhaobiao_gg","http://www.szggzyjy.cn/szfront/jyxx/002005/002005001/?Paging=1",["name","ggstart_time","href","info"],f4,f5],


]




if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000

def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省宿州市",**args)
    est_html(conp,f=f3,**args)

# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None



if __name__=='__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "anhui", "suzhou"]

    work(conp=conp,cdc_total=None)

