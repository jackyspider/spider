from lxml import etree

with open('python-requests.html','rb') as f:
    html = f.read()
print(type(html))


tree = etree.HTML(html)

print(tree.xpath('//html/head/title/text()')[0])
print(tree.cssselect('html > head > title ')[0].text)


