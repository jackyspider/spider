#!/usr/bin/env python
# __author__: vincentlc

import scrapy
from proxy_pool.items import ProxyPoolItem


class MimiipSpider(scrapy.Spider):
    name = "mimiip"
    allowed_domains = ["mimiip.com"]

    def start_requests(self):
        yield scrapy.Request("http://www.mimiip.com/gngao", meta={'level': 1})
        yield scrapy.Request("http://www.mimiip.com/gnpu", meta={'level': 1})
        yield scrapy.Request("http://www.mimiip.com/gntou", meta={'level': 1})
        yield scrapy.Request("http://www.mimiip.com/hw", meta={'level': 1})

    def parse(self, response):

        iplist = response.xpath('//table/tr')
        page_number = response.xpath("//div[@class='pagination']/a[last()-1]/text()").extract_first()
        level = response.meta['level']

        for x in iplist[1:-1]:
            ips = x.xpath('td[1]/text()').extract_first()
            ports = x.xpath('td[2]/text()').extract_first()
            protocols = x.xpath('td[5]/text()').extract_first()
            types = x.xpath('td[4]/text()').extract_first()

            province = x.xpath('td[3]/a[1]/text()').extract_first()
            city = x.xpath('td[3]/a[2]/text()').extract_first()
            address = ""
            if city is not None:
                address = province + city
            else:
                address = province

            yield ProxyPoolItem({
                'ip': ips,
                'protocol': protocols,
                'port': ports,
                'types': types,
                'address': address,
                'website': 'www.mimiip.com'
            })

        if level == 1 and page_number is not None:
            url = response.url
            for i in range(2, int(page_number) + 1):
                yield scrapy.Request("{0}/{1}".format(url, i), meta={'level': 2})
