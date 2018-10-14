# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from proxy_pool.items import ProxyPoolItem


class IphaiSpider(scrapy.Spider):
    name = 'iphai'
    allowed_domains = ['iphai.com']
    start_urls = ['http://www.iphai.com/free/ng',
    'http://www.iphai.com/free/np',
    'http://www.iphai.com/free/wg',
    'http://www.iphai.com/free/wp']

    def parse(self, response):
        data = response.xpath('//table[@class="table table-bordered table-striped table-hover"]/tr')
        if data:
            for x in data[1:]:
                item = ProxyPoolItem()
                info = x.xpath('td/text()').extract()
                item['ip'] = info[0].strip()
                item['protocol'] = info[3].strip()
                item['port'] = info[1].strip()
                item['types'] = info[2].strip()
                item['address'] = info[4].strip()
                item['website'] = 'iphai.com'
                yield item