# -*- coding: utf-8 -*-
import scrapy
from proxy_pool.items import ProxyPoolItem

class BaizhongsouSpider(scrapy.Spider):
    name = 'baizhongsou'
    allowed_domains = ['baizhongsou.com']
    start_urls = ['http://ip.baizhongsou.com/']

    def parse(self, response):
        info = response.xpath('//div[@class="daililist"]/table/tr')
        for x in info[1::2]:
            item = ProxyPoolItem()
            data = x.xpath('td/text()').extract()
            item['ip'] = data[0].split(':')[0]
            item['protocol'] = 'HTTP'
            item['port'] = data[0].split(':')[1]
            item['address'] = data[1]
            item['website'] = 'baizhongsou.com'
            item['types'] = '普通'
            yield item
