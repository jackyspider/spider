# -*- coding: utf-8 -*-
import scrapy
import re
from proxy_pool.items import ProxyPoolItem

class KxdailiSpider(scrapy.Spider):
    name = 'kxdaili'
    allowed_domains = ['kxdaili.com']

    def start_requests(self):
        for i in range(1, 3):
            for j in range(1, 11):
                yield scrapy.Request("http://www.kxdaili.com/dailiip/{0}/{1}.html#ip".format(i, j),
                                     callback=self.parse)

    def parse(self, response):
        all_data = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>\s+<td>([^<]+)</td>\s+<td>([^<]+)</td>\s+<td>([^<]+)</td>\s+<td>([^<]+)</td>', response.text)
        for each in all_data:
            yield ProxyPoolItem({
                'ip': each[0],
                'port': each[1],
                'types': each[2],
                'protocol': each[3],
                'address': each[5],
                'website': 'www.kxdaili.com'
                })
