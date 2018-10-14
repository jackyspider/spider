# -*- coding: utf-8 -*-
import scrapy
import string
from scrapy import Selector
from proxy_pool.items import ProxyPoolItem

class GoubanjiaSpider(scrapy.Spider):
    name = 'goubanjia'
    allowed_domains = ['goubanjia.com']
    start_urls = ['http://www.goubanjia.com/free/index{}.shtml'.format(i) for i in range(1, 11)]

    def parse(self, response):
        data = response.xpath('//*[@id="list"]/table/tbody/tr')
        if data : 
            for x in data :
               item = ProxyPoolItem()
               info = x.xpath('td')
               ipport = x.xpath('td[1]//*[name(.)!="p"]/text()').extract()
               address = x.xpath('td[4]//*[name(.)="a"]/text()').extract()
               item['ip'] = "".join(ipport[:-1])
               item['port'] = ipport[-1]
               item['protocol'] = info[2].xpath('string(.)').extract()[0]
               item['types'] = info[1].xpath('string(.)').extract()[0] 
               item['address'] = "".join(address)
               item['website'] = 'goubanjia.com'
               yield item
