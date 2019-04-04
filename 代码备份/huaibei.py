import time
from os.path import join, dirname

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
#
# url="http://www.hbzbcg.cn/hbweb/jyxx/002001/002001005/002001005001/MoreInfo.aspx?CategoryNum=002001005001"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



_name_='huaibei'


def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        driver.find_element_by_xpath('//div[@class="main3"]/table/tbody/tr/td[3]/table/tbody/tr[1]/'
                                     'td[2]/table/tbody/tr/td[2]/font[2]/a[3]').click()

        locator = (By.XPATH, '//*[@id="container"]/div[4]/table/tbody/tr/td[3]/table/tbody/tr[2]/'
                             'td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('(//font[@class="MoreinfoColor"])[{}]'.format(i)).click()

        locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))

        locator = (
            By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def f1(driver,num):

    #记录第一种情况的总页码
    global PAGE
    page_one=PAGE[0]

    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text=driver.find_element_by_xpath('(//td[@align="left"])[2]/font[2]/a[4]/font').text

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
    # print(len(trs))

    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']
        if '</font>' in name:
            if name.startswith('<font'):
                name = re.findall(r'</font>(.+)', name)[0]
            else:
                name = re.findall(r'(.+)<font', name)[0]
        ggstart_time = tds[2].get_text().strip()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.hbzbcg.cn' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df




def f2(driver):
    url = driver.current_url
    global PAGE
    global CC_TEXT
    PAGE=[]
    CC_TEXT=[]
    new_url=re.findall('http://www.hbzbcg.cn/hbweb/jyxx/\d+?/\d+?/',url)[0]

    driver.get(new_url)
    locator = (By.XPATH, '(//td[@class="TDStyle"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    more_num = soup.find_all('font', class_="MoreinfoColor")
    more = len(more_num)
    total=0
    for num in range(1,more+1):
        driver.get(new_url)
        locator = (By.XPATH, '(//font[@class="MoreinfoColor"])[{}]'.format(num))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        total_=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
        cc_text=driver.find_element_by_xpath('(//td[@align="left"])[2]/font[2]/a[4]/font').text

        PAGE.append(int(total_))
        CC_TEXT.append(cc_text)
        total += int(total_)

    total = int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH,'//td[@class="infodetd"] | //div[@id="menutab_6_1"]')

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

    div = soup.find('td', attrs={'id': "TDContent"})
    if div == None:
        div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})
        if div == None:
            raise ValueError

    return div



data=[
    ["gcjs_zhaobiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=002001001001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_gqita_da_bian_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001003/002001003001/MoreInfo.aspx?CategoryNum=002001003001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001005/002001005001/MoreInfo.aspx?CategoryNum=002001005001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001002/002001002001/MoreInfo.aspx?CategoryNum=002001002001",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002002/002002001/002002001001/MoreInfo.aspx?CategoryNum=002002001001",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_gqita_da_bian_gg","http://www.hbzbcg.cn/hbweb/jyxx/002002/002002003/002002003001/MoreInfo.aspx?CategoryNum=002002003001",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002002/002002002/002002002001/MoreInfo.aspx?CategoryNum=002002002001",["name","ggstart_time","href","info"],f1,f2],

]


if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000

def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省淮北市",**args)
    est_html(conp,f=f3,**args)


# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None


if __name__=='__main__':

    work(conp=["postgres","since2015","192.168.3.171","anhui","huaibei"],cdc_total=None)