# -*- coding: utf-8 -*-
import scrapy
import re
from proxy_pool.items import ProxyPoolItem

class YundailiSpider(scrapy.Spider):
    name = 'yundaili'
    allowed_domains = ['yun-daili.com']
    start_urls = ["http://www.yun-daili.com/free.asp?page=1"]

    def parse(self, response):
        page = re.findall('<strong><font color="red">(\d+)</font>/(\d+)</strong>', response.text)
        ips = re.findall('<td class="style1">(\d+\.\d+\.\d+\.\d+)</td>', response.text)
        ports = re.findall('<td class="style2">(\d+)</td>', response.text)
        types = re.findall('<td class="style3">([^<]+)</td>',response.text)
        addresses = re.findall('<td class="style5">([^<]+)</td>', response.text)
        protocols = re.findall('<td class="style4">([^<]+)</td>', response.text)
        if page:
            now_page, count_all = page[0]
            for ip, port, typ, address, protocol in zip(ips, ports, types, addresses, protocols):
                yield ProxyPoolItem({
                    'ip': ip,
                    'protocol': protocol,
                    'types': typ,
                    'port': port,
                    'address': address,
                    'website': 'www.yun-daili.com'
                })
            _next = int(now_page) + 1 
            _next_url = re.sub('page=(\d+)', "page="+str(_next), response.url)
            yield scrapy.Request(_next_url, self.parse)
