# -*- coding: utf-8 -*-
import scrapy
from proxy_pool.items import ProxyPoolItem


class A3464Spider(scrapy.Spider):
    name = '3464'
    allowed_domains = ['3464.com']
    start_urls = ['http://www.3464.com/data/Proxy/http/']

    def parse(self, response):
        info = response.xpath('//div[@class="CommonBody"]/table[6]/tr[4]/td/table/tr')
        for x in info[1:]:
            item = ProxyPoolItem()
            data = x.xpath('td/text()').extract()
            try:
                item['ip'] = data[0]
            except IndexError:
                continue
            item['protocol'] = 'HTTP'
            item['port'] = data[1]
            item['address'] = x.xpath('td/div/text()').extract()[0]
            item['types'] = data[2]
            item['website'] = '3464.com'
            yield item

