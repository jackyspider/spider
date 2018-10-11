import requests
from lxml import etree

# url = 'http://www.python-requests.org/en/master/'
#
# with requests.get(url) as resp:
#     html = resp.content
#
# with open("python-requests.html",'wb') as f:
#     f.write(html)

with open('python-requests.html','rb') as f:
    html = f.read()
print(type(html))


tree = etree.HTML(html)
print(type(tree))

# content = tree.xpath('//*[@id="requests-http-for-humans"]/h1/text()')
content = tree.xpath('//h1/text()')
print(content[0])

toctree = tree.xpath('//*[@id="the-user-guide"]/div/ul/li/a/text()')
for toc in toctree:
    # print(toc.xpath('string(.)'))
    print(toc)