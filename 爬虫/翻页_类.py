import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import json

class Doubantop(object):

    def __init__(self):
        self.baseurl = 'https://movie.douban.com/top250'
        self.result_list = []

    def start_requests(self, url):
        r = requests.get(url)
        return r.content

    def parse(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        movie_list = soup.find_all('div', class_ = 'item')
        for movie in movie_list:
            mydict = {}
            mydict['title'] = movie.find('span', class_ = 'title').text
            mydict['score'] = movie.find('span', class_ = 'rating_num').text
            quote = movie.find('span', class_ = 'inq')
            mydict['quote'] = quote.text if quote else None 
            star = movie.find('div', class_ = 'star')
            mydict['comment_num'] = star.find_all('span')[-1].text[:-3]
            self.result_list.append(mydict)
			
		#寻找下一页链接
        nextpage = soup.find('span', class_ = 'next').a
        if nextpage:
            nexturl = self.baseurl + nextpage['href']
            text = self.start_requests(nexturl)
            self.parse(text)

			
    def write_json(self, result):
        s = json.dumps(result, indent = 4, ensure_ascii=False)
        with open('movies.json', 'w', encoding = 'utf-8') as f:
            f.write(s)

    def start(self):
        text = self.start_requests(self.baseurl)
        self.parse(text)
        self.write_json(self.result_list)

douban = Doubantop()
douban.start()