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
from zhulong.util.conf import get_conp
# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="http://www.szggzyjy.cn/szfront/jyxx/002001/002001001/002001001001/"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_='chizhou'

def chang_address(driver,i,c_text):

    ##CC_TEXT包含县区的列表
    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        driver.find_element_by_xpath(
            '(//font[@color="#17a8e4"])/../../../following-sibling::tr[1]/td/table/tbody/tr[2]/td/a').click()
        locator = (By.XPATH, '(//h4[@class="s-block-title"])[1]/a[2]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('(//h4[@class="s-block-title"])[{}]/a[2]'.format(i - 1)).click()
        locator = (By.XPATH, '//div[@id="Paging"]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//li[@class="wb-data-list"][1]/div/a').get_attribute('href')[-60:-30]
        #翻页
        driver.execute_script("window.location.href='./?Paging={}'".format(num))

        locator = (By.XPATH, '//li[@class="wb-data-list"][1]/div/a[not(contains(@href,"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):

    #PAGE中包含各个类型页面的总页数

    locator = (By.XPATH, '//li[@class="wb-data-list"][1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/a').text.strip()

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
    lis = soup.find_all('li', class_="wb-data-list")

    for tr in lis:
        href = tr.div.a['href']
        name = tr.div.a['title']
        ggstart_time = tr.span.get_text().strip(']').strip('[')
        if 'http' in href:
            href = href
        else:
            href = "http://ggj.chizhou.gov.cn"+href

        info={'address':CC_TEXT[i-1].strip('项目')}
        info=json.dumps(info,ensure_ascii=False)
        tmp = [name, ggstart_time, href,info]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    # df["info"] = None
    return df



def f2(driver):
    global PAGE
    global CC_TEXT
    CC_TEXT=[]
    PAGE=[]
    locator = (By.XPATH, '//li[@class="wb-data-list"][1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    for i in range(1, 6):
        if i != 1:
            driver.find_element_by_xpath(
                '(//font[@color="#17a8e4"])/../../../following-sibling::tr[1]/td/table/tbody/tr[2]/td/a').click()
            locator = (By.XPATH, '(//h4[@class="s-block-title"])[1]/a[2]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_xpath('(//h4[@class="s-block-title"])[{}]/a[2]'.format(i - 1)).click()
            locator = (By.XPATH, '//div[@id="Paging"]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        try:
            page = driver.find_element_by_xpath('//td[@class="huifont"]').text
            total_ = re.findall(r'/(\d+)', page)[0]
        except:
            total_ = 0
        cc_text = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/a').text.strip()
        total_=int(total_)
        PAGE.append(total_)
        CC_TEXT.append(cc_text)

    total = int(sum(PAGE))
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH,
               '/html/body')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    html=driver.page_source
    if '系统发生了错误' in html:

        return '404'

    locator = (By.XPATH, '//div[contains(@id,"menutab_6") and (not(@style) or @style="")][string-length()>10] | //div[@class="ewb-tell-bd"]/table | //*[@id="form1"]/div[4]/div/div[2]/div/table/tbody/tr/td/table')

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
        div = soup.find('div', class_="ewb-tell-bd").find_all('tr')[2]
    except:
        div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})
        if div==None:
            raise ValueError

    return div




data=[
    ["gcjs_yvcai_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001007/002001007001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhaobiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001002/002001002001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001003/002001003001/",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_gqita_da_bian_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001005/002001005001/",["name","ggstart_time","href","info"],f1,f2],

    #包含预采和单一性来源
    ["zfcg_gqita_yu_dan_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002005/002002005001/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002001/002002001001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_liubiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002007/002002007001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002003/002002003001/",["name","ggstart_time","href","info"],f1,f2],
    #包含答疑和变更
    ["zfcg_gqita_da_bian_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002004/002002004001/",["name","ggstart_time","href","info"],f1,f2],

]





if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 2
else:
    CDC_NUM = 10000


def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省池州市",**args)
    est_html(conp,f=f3,**args)


# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None



if __name__=='__main__':

    work(conp=["postgres", "since2015", "192.168.3.171", "anhui", "chizhou"],cdc_total=None,headless=False,num=1)

