# -*- coding: utf-8 -*-
import scrapy
import re
from proxy_pool.items import ProxyPoolItem


class CoderbusySpider(scrapy.Spider):
    name = 'coderbusy'
    allowed_domains = ['coderbusy.com']
    start_urls = ['https://proxy.coderbusy.com/']

    def parse(self, response):
        s = response.text	
        r = re.compile(r'<tr>[\s\S]*?<\/tr>', re.I|re.M)
        d = r.findall(s)
        for each in d[1:]:
            yield ProxyPoolItem({
				'ip': re.findall(r'\d+\.\d+\.\d+\.\d+', each)[0],
				'port': re.findall(r'<td>(\d+)<\/td>', each)[0],
				'types': re.findall(r'<td>([\s\S]*?)<\/td>', each)[6],
				'protocol': re.findall(r'<td>([\s\S]*?)<\/td>', each)[4],
				'address': re.findall(r'\.aspx">([^<]+)<\/a>', each)[0],
				'website': 'https://proxy.coderbusy.com/'
			})