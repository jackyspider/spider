from bs4 import BeautifulSoup


html = """
<html>
    <head>
        <title> bs4 demo </title>
    </head>
    <body>
        <div class='red' id='id_demo'> <p> <span>Hello</span>  world </p> 
        <a> 新闻 </a>

        </div>
        
        <div class="blue" > bbbbbb </div>
    
    </body>
</html>

"""
soup = BeautifulSoup(html,'lxml')
# 1.按tag查找
print(soup.get_text())
print(soup.title.get_text())
#
# print('\n'.join(dir(soup)))
# print('---------------')
# print('\n'.join(dir(soup.div)))

soup.body.a
soup.a

# 2.find
soup.find(name='a')
soup.find(name='body').find(name='a')

# 3. 获取元素文本
print(soup.div.p.get_text())
print(soup.div.p.span.string)


# 4. 获取属性值
print(soup.div.attrs)
print(soup.div.get('id'))

# 5.find_all  findAll

soup.find_all(name='div',attrs={},recursive=True,text='',class_='',limit=2)

"""
-name : tag name
- attrs : tag的属性
- recursive: 是否递归
- text 按tag显示的内容查找
- limit  : 限制找到的结果的个数
"""
soup.find_all(name='div',attrs={},recursive=True,text='',class_='',limit=1)
soup.find(name='div',attrs={},recursive=True,text='',class_='')

print(soup.find(name='div',attrs={'class':'blue'}))



































