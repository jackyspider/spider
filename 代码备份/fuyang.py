import time
from collections import OrderedDict
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

from zhulong.util.etl import est_tbs, est_meta, est_html, gg_existed, add_info

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]
from zhulong.util.conf import get_conp

# url="http://www.hbzbcg.cn/hbweb/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=002001001001"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_='fuyang'


def chang_address(driver,i,c_text):

    # 不是对应的的都要点击
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        #返回汇总页
        driver.find_element_by_xpath('//*[@id="right"]/div[1]/div/a[3]').click()

        locator = (By.XPATH, '//*[@id="right"]/div[2]/div/ul[1]/li[1]/div/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        #点击对应地区
        driver.find_element_by_xpath(
            '(//a[@class="block-more"])[{}]'.format(i)).click()
        locator = (By.XPATH, '//*[@id="right"]/div[2]/div[1]/div/ul/li[1]/div/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]

    #第一页不用翻页
    if int(cnum) != num:
        val = driver.find_element_by_xpath(
            '//li[@class="wb-data-list"][1]/div/a').text
        #翻页
        driver.execute_script("window.location.href='./?Paging={}'".format(num))
        # 第二个等待
        locator = (By.XPATH,
                   '//li[@class="wb-data-list"][1]/div/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def f1(driver,num):

    #PAGE中包含各个类型页面的总页数
    global PAGE
    # print(PAGE)

    locator = (By.XPATH, '//*[@id="right"]/div[2]/div[1]/div/ul/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('//*[@id="right"]/div[1]/a').text

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
    lis = soup.find_all('li', class_='wb-data-list')

    for tr in lis:
        href = tr.div.a['href']
        name = tr.div.a['title']
        ggstart_time = tr.span.get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://jyzx.fy.gov.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df




def f2(driver):
    global PAGE
    global CC_TEXT
    PAGE=[]
    CC_TEXT=[]

    locator = (By.XPATH, '//*[@id="right"]/div[2]/div[1]/div/ul/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 点回汇总页
    driver.find_element_by_xpath('//*[@id="right"]/div[1]/div/a[3]').click()

    locator = (By.XPATH, '//*[@id="right"]/div[2]/div/ul[1]/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    all_more = soup.find_all('a', class_='block-more')
    all_more = int(len(all_more))

    total = 0
    for i in range(1, all_more + 1):

        driver.find_element_by_xpath(
            '(//a[@class="block-more"])[{}]'.format(i)).click()
        locator = (By.XPATH, '//*[@id="right"]/div[2]/div[1]/div/ul/li[1]/div/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        try:
            page = driver.find_element_by_xpath('//td[@class="huifont"]').text
            total_ = re.findall(r'/(\d+)', page)[0]
        except:
            total_ = 0
        cc_text = driver.find_element_by_xpath('//*[@id="right"]/div[1]/a').text


        driver.find_element_by_xpath('//*[@id="right"]/div[1]/div/a[3]').click()
        locator = (By.XPATH, '//*[@id="right"]/div[2]/div/ul[1]/li[1]/div/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        total = total + int(total_)

        PAGE.append(int(total_))
        CC_TEXT.append(cc_text)

    driver.quit()
    
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '/html/body')
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    html = driver.page_source
    if '系统出现了错误' in html:
        return '404'
    locator = (By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/table | /html/body/div[2]/div[2]/div[2]/div')

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
        div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})

    return div





data=[
    ["gcjs_zhaobiao_gg","http://jyzx.fy.gov.cn/FuYang/jsgc/012001/012001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://jyzx.fy.gov.cn/FuYang/jsgc/012006/012006001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://jyzx.fy.gov.cn/FuYang/jsgc/012002/012002001/",["name","ggstart_time","href","info"],f1,f2],
  # # #包含变更和变更中标人，中标候选人
    ["gcjs_gqita_bian_gg","http://jyzx.fy.gov.cn/FuYang/jsgc/012003/012003001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_gqita_da_bian_gg","http://jyzx.fy.gov.cn/FuYang/jsgc/012004/012004001/",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_jiaotong_zhaobiao_gg","http://jyzx.fy.gov.cn/FuYang/jtys/013001/013001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_jiaotong_zhongbiaohx_gg","http://jyzx.fy.gov.cn/FuYang/jtys/013006/013006001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_jiaotong_zhongbiao_gg","http://jyzx.fy.gov.cn/FuYang/jtys/013002/013002001/",["name","ggstart_time","href","info"],f1,f2],
   # ### #包含变更和变更中标人，中标候选人
    ["gcjs_jiaotong_gqita_bian_gg","http://jyzx.fy.gov.cn/FuYang/jtys/013003/013003001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_jiaotong_gqita_da_bian_gg","http://jyzx.fy.gov.cn/FuYang/jtys/013004/013004001/",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_shuili_zhaobiao_gg","http://jyzx.fy.gov.cn/FuYang/slgc/014001/014001001/",["name","ggstart_time","href","info"],f1,f2],
    ##颍上县4,5页有问题
    ["gcjs_shuili_zhongbiaohx_gg","http://jyzx.fy.gov.cn/FuYang/slgc/014006/014006001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_shuili_zhongbiao_gg","http://jyzx.fy.gov.cn/FuYang/slgc/014002/014002001/",["name","ggstart_time","href","info"],f1,f2],
   ### #包含变更和变更中标人，中标候选人
    ["gcjs_shuili_gqita_bian_gg","http://jyzx.fy.gov.cn/FuYang/slgc/014003/014003001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_shuili_gqita_da_bian_gg","http://jyzx.fy.gov.cn/FuYang/slgc/014004/014004001/",["name","ggstart_time","href","info"],f1,f2],

    #临泉市第六页有问题
    ["zfcg_zhaobiao_gg","http://jyzx.fy.gov.cn/FuYang/zfcg/011001/011001001/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_biangen_gg","http://jyzx.fy.gov.cn/FuYang/zfcg/011004/011004001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://jyzx.fy.gov.cn/FuYang/zfcg/011002/011002001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_yvcai_gg","http://jyzx.fy.gov.cn/FuYang/zfcg/011003/011003001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiao_danyilaiyuan_gg","http://jyzx.fy.gov.cn/FuYang/zfcg/011007/011007001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_jinkou_gg","http://jyzx.fy.gov.cn/FuYang/zfcg/011008/011008001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_gqita_da_bian_gg","http://jyzx.fy.gov.cn/FuYang/zfcg/011005/011005001/",["name","ggstart_time","href","info"],f1,f2],

    ["qsy_zhaobiao_gg","http://jyzx.fy.gov.cn/FuYang/shfw/017001/017001001/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_zhongbiao_gg","http://jyzx.fy.gov.cn/FuYang/shfw/017002/017002001/",["name","ggstart_time","href","info"],f1,f2],
    ####包含流标，变更
    ["qsy_gqita_liu_bian_gg","http://jyzx.fy.gov.cn/FuYang/shfw/017003/017003001/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_gqita_da_bian_gg","http://jyzx.fy.gov.cn/FuYang/shfw/017004/017004001/",["name","ggstart_time","href","info"],f1,f2],

]





if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000

def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省阜阳市",**args)
    est_html(conp,f=f3,**args)

# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None


if __name__=='__main__':

    work(conp=["postgres","since2015","192.168.3.171","anhui","fuyang"],cdc_total=None,headless=False,num=1)