# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from proxy_pool.items import ProxyPoolItem

class KuaiSpider(scrapy.Spider):
    name = 'kuai'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['http://www.kuaidaili.com/free/inha/1/',
                  'http://www.kuaidaili.com/free/intr/1/']

    def parse(self, response):
        typee, now_page = re.findall('com/free/(.*?)/(\d+)/', response.url)[0]
        iplist = response.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        if iplist:
            for x in iplist:
                data = x.xpath('td/text()').extract()
                item = ProxyPoolItem()
                item['ip'] = data[0]
                item['protocol'] = data[3]
                item['port'] = data[1]
                item['types'] = data[2]
                item['address'] = data[4]
                item['website'] = 'www.kuaidaili.com'
                yield item
            next_page = int(now_page) + 1
            next_url = 'http://www.kuaidaili.com/free/{}/{}/'.format(typee, next_page)
            yield Request(next_url, self.parse)


