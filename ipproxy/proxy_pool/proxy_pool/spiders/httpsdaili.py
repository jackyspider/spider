# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from proxy_pool.items import ProxyPoolItem

class HttpsdailiSpider(scrapy.Spider):
    name = 'httpsdaili'
    allowed_domains = ['httpsdaili.com']
    start_urls = ['http://www.httpsdaili.com/?stype=1',
                  'http://www.httpsdaili.com/?stype=2',
                  'http://www.httpsdaili.com/?stype=3',
                  'http://www.httpsdaili.com/?stype=4']


    def parse(self, response):
        info = response.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        if info:
            for d in info:
                item = ProxyPoolItem()
                data = d.xpath('td/text()').extract()
                item['ip'] = data[0]
                item['protocol'] = data[3]
                item['port'] = data[1]
                item['types'] = data[2]
                item['address'] = data[4]
                item['website'] = 'httpsdaili.com'
                yield item
            next_url = response.xpath('//div[@id="listnav"]/ul/a/@href').extract()[-2]
            yield Request('http://www.httpsdaili.com/'+next_url, self.parse)
