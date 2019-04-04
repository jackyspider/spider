from os.path import dirname, join

import pandas as pd
import re 

from selenium import webdriver 
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

import sys 
import time

import json
from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed



# driver=webdriver.Chrome()

# url="""http://jyzx.yiyang.gov.cn/jyxx/003001/003001001/2.html"""

# driver.get(url)

_name_='huangshan'


def f1(driver,num):

    locator = (By.XPATH, '(//div[@class="content"])[2]//tr[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    main_url = url.rsplit('=', maxsplit=1)[0]

    cnum=re.findall(r'Paging=(\d+)',url)[0]

    if cnum != str(num):

        url=main_url + '='+str(num)
        val = driver.find_element_by_xpath('(//div[@class="content"])[2]//tr[1]//a').get_attribute('href')
        driver.get(url)

        # 第二个等待
        locator = (
        By.XPATH, '(//div[@class="content"])[2]//tr[1]//a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all('div', class_='content')[1]
    table = div.find('table')
    trs = table.find_all('tr')

    for tr in trs:

        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a.get_text()
        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.hscgw.gov.cn' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=None
    return df 


def f2(driver):
    locator = (By.XPATH, '(//div[@class="content"])[2]//tr[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//td[@class="huifont"]').text

    total = re.findall('/(\d+)', page)[0]
    total = int(total)

    driver.quit()
    return total


def f3(driver,url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="main"]')

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

    div = soup.find('div', attrs={'id': re.compile('menutab_5_\d'), 'style': ''})
    if div == None:
        div = soup.find('div', attrs={'id': re.compile('menutab_4_\d'), 'style': ''})
        if div==None:
            div=soup.find('td',id='TDContent')
            if div==None:
                raise ValueError

    return div




data=[
    ["gcjs_zhaobiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_zhongbiaohx_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001008/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001005/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_liubiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001006/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_xiaoxing_zhaobiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001007/004001007001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_xiaoxing_zhongbiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001007/004001007003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_xiaoxing_liubiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001007/004001007004/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_xiaoxing_zhongbiaohx_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001007/004001007005/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_xiaoxing_bixuan_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004001/004001007/004001007006/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004002/004002003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004002/004002004/?Paging=1",["name","ggstart_time","href","info"],f1,f2],


    ["zfcg_zhongbiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004002/004002006/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_liubiao_gg","http://www.hscgw.gov.cn/hsweb/jyxx/004002/004002007/?Paging=1",["name","ggstart_time","href","info"],f1,f2],


]



def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省黄山市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':


    work(conp=["postgres","since2015","192.168.3.171","anhui","huangshan"])

