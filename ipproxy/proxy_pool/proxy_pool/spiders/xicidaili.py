# -*- coding: utf-8 -*-
import scrapy
import re
from proxy_pool.items import ProxyPoolItem


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidali.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        ips = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>', response.text)
        ports = re.findall('<td>(\d+)</td>', response.text)
        types = re.findall('<td class="country">([^<]+)</td>', response.text)
        protocols = re.findall('<td>(HTTPS?)</td>', response.text)
        for ip, port, _type, protocol in zip(ips, ports, types, protocols):
            yield ProxyPoolItem({
                'website': 'xicidaili',
                'ip': ip,
                'protocol': protocol,
                'port': port,
                'types': _type
            })
