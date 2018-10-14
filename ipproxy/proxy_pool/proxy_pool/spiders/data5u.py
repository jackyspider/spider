# -*- coding: utf-8 -*-
# __author__: vincentlc

import scrapy
from proxy_pool.items import ProxyPoolItem


class Data5uSpider(scrapy.Spider):
    name = "data5u"
    allowed_domains = ["data5u.com"]

    def start_requests(self):
        yield scrapy.Request("http://www.data5u.com/free/gngn/index.shtml")
        yield scrapy.Request("http://www.data5u.com/free/gnpt/index.shtml")
        yield scrapy.Request("http://www.data5u.com/free/gwgn/index.shtml")
        yield scrapy.Request("http://www.data5u.com/free/gwpt/index.shtml")

    def parse(self, response):

        iplist = response.xpath('//ul[@class="l2"]')

        for x in iplist[1:-1]:
            ip = x.xpath('span[1]/li/text()').extract_first()
            port = x.xpath('span[2]/li/text()').extract_first()
            protocol = str(x.xpath('span[4]/li/a/text()').extract_first()).upper()
            type = x.xpath('span[3]/li/a/text()').extract_first()

            city = x.xpath('span[6]/li/a/text()').extract_first()
            country = x.xpath('//ul[@class="l2"][1]/span[5]/li/a/text()').extract_first()
            address = ""
            if city is not None:
                address = country + city
            else:
                address = country

            yield ProxyPoolItem({
                'ip': ip,
                'protocol': protocol,
                'port': port,
                'types': type,
                'address': address,
                'website': 'www.data5u.com'
            })

