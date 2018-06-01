import json

import requests


class Douban(object):
    def __init__(self):
        self.base_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=悬疑&sort=recommend&page_limit=20&page_start={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Referer': 'https://movie.douban.com/explore'
        }
        self.page_start = 0
        # 每次翻页如果都打开文件的话,加大了负载消耗
        self.file = open('doubanmovie.json','w')


    def run(self):
        while True:
            json_str = self.get_data()
            movie_list = self.parse_data(json_str)
            self.save_data(movie_list)
            self.page_start += 20
            if movie_list == []:
                break


    def get_data(self):
        url = self.base_url.format(self.page_start)
        response = requests.get(url,headers=self.headers)
        return response.content    # 忘了响应内容需要处理了

    def parse_data(self,json_str):
        # json数据加载成python的字典
        dict = json.loads(json_str)
        # print(type(dict))
        # print(dict)
        # print(dict['subjects'])
        list = dict['subjects']
        movie_list = []
        for data in list:
            dict_data = {}

            dict_data['title'] = data['title']
            dict_data['url'] = data['url']
            dict_data['image'] = data['cover']
            movie_list.append(dict_data)
        # print(movie_list)
        return movie_list

    def save_data(self, movie_list):
        for movie in movie_list:
            json_data = json.dumps(movie,ensure_ascii=False) + ',\n'
            self.file.write(json_data)
    def __del__(self):
        self.file.close()


if __name__ == '__main__':
    douban = Douban()
    douban.run()