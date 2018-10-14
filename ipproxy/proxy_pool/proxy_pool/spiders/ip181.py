# -*- coding: utf-8 -*-
import scrapy
import re
from proxy_pool.items import ProxyPoolItem

class Ip181Spider(scrapy.Spider):
    name = 'ip181'
    allowed_domains = ['ip181.com']
    start_urls = ["http://www.ip181.com/"]

    def parse(self, response):
        all_data = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>\s+<td>([^<]+)</td>\s+<td>([^<]+)</td>\s+<td>([^<]+)</td>\s+<td>([^<]+)</td>', response.text)
        for each in all_data:
            yield ProxyPoolItem({
                'ip': each[0],
                'port': each[1],
                'types': each[2],
                'protocol': each[3],
                'address': each[5],
                'website': 'www.ip181.com'
                })
