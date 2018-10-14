import scrapy
import os
import sys
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import importlib


def remove(target_list, remove_list):
    for i in remove_list:
        if i in target_list:
            target_list.remove(i)


def filter(classes):
    for item in classes:
        if item.endswith('Spider'):
            return item


def start():
    sys.path.append('./proxy_pool/spiders/')
    files = os.listdir('./proxy_pool/spiders/')
    remove(files, ['__init__.py', '__pycache__'])
    runner = CrawlerRunner(get_project_settings())
    configure_logging()
    for file in files:
        module = importlib.import_module(file.split('.')[0])
        classes = dir(module)
        remove(classes, ['__builtins__', '__cached__', '__doc__', '__file__',
                         'ProxyPoolItem', '__loader__', '__name__', '__package__', '__spec__', 'scrapy'])
        runner.crawl(getattr(module, filter(classes)))
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

start()
