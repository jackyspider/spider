# -*- coding: utf-8 -*-
import scrapy
from proxy_pool.items import ProxyPoolItem
from scrapy.http import Request


class Ip3366Spider(scrapy.Spider):
    name = 'ip3366'
    allowed_domains = ['ip3366.net']
    start_urls = ['http://www.ip3366.net/free/?stype=1',
                  'http://www.ip3366.net/free/?stype=2',
                  'http://www.ip3366.net/free/?stype=3',
                  'http://www.ip3366.net/free/?stype=4']

    def parse(self, response):
        info = response.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for x in info:
            item = ProxyPoolItem()
            data = x.xpath('td/text()').extract()
            item['ip'] = data[0]
            item['protocol'] = data[3]
            item['port'] = data[1]
            item['address'] = data[5]
            item['website'] = 'ip3366.com'
            item['types'] = data[2]
            yield item
        next_url = response.xpath('//div[@id="listnav"]/ul/a/@href').extract()
        if next_url:
            yield Request('http://www.ip3366.net/'+next_url[-2], self.parse)

