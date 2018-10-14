# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Selector
from proxy_pool.items import ProxyPoolItem

class XdailiSpider(scrapy.Spider):
    name = 'xdaili'
    allowed_domains = ['xdaili.cn']
    start_urls = ['http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10']

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        if data :
             for x in data['RESULT']['rows'] :
                 item = ProxyPoolItem()
                 item['ip'] = x['ip']
                 item['port'] = x['port']
                 item['protocol'] = x['type']
                 item['types'] = x['anony']
                 item['address'] = x['position']
                 item['website'] = 'xdaili.cn'
                 yield item

