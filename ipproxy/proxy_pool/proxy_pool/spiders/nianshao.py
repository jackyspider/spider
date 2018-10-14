# -*- coding: utf-8 -*-
import scrapy
import re
from proxy_pool.items import ProxyPoolItem

class NianshaoSpider(scrapy.Spider):
    name = 'nianshao'
    allowed_domains = ['nianshao.me']
    start_urls = ["http://www.nianshao.me/?stype=1&page=1", 
                  "http://www.nianshao.me/?stype=2&page=1"]

    def parse(self, response):
        page = re.findall('<strong><font color="#49afcd">(\d+)</font>/(\d+)</strong>', response.text)
        ips = re.findall('<td style="WIDTH:110PX">(\d+\.\d+\.\d+\.\d+)</td>', response.text)
        ports = re.findall('<td style="WIDTH:40PX">(\d+)</td>', response.text)
        types = re.findall(u"<td style=\"WIDTH:55PX\">([\u4e00-\u9fa5]+)</td>",response.text)
        addresses = re.findall(u"<td style=\"WIDTH:135PX\">([[\u4e00-\u9fa5]+)</td>", response.text)
        protocols = re.findall('<td style="WIDTH:55PX">(HTTPS?)</td>', response.text)
        if page:
            now_page, count_all = page[0]
            for ip, port, typ, address, protocol in zip(ips, ports, types, addresses, protocols):
                yield ProxyPoolItem({
                    'ip': ip,
                    'protocol': protocol,
                    'types': typ,
                    'port': port,
                    'address': address,
                    'website': 'www.nianshao.me'
                })
            _next = int(now_page) + 1 
            _next_url = re.sub('page=(\d+)', "page="+str(_next), response.url)
            yield scrapy.Request(_next_url, self.parse)
