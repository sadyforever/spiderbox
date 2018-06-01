import os
from lxml import etree

import requests


class tiebaDetailImage(object):

    def __init__(self,tieba):
        self.url = 'https://tieba.baidu.com/f/good?kw={}&cid=1'
        self.headers =  {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': 'tieba.baidu.com',
            'Cookie': 'BAIDUID=C95F4EB2802449AE1F812CC158E40C58:FG=1; BIDUPSID=C95F4EB2802449AE1F812CC158E40C58; PSTM=1520245998; TIEBA_USERTYPE=6f0cc0f466b909d65f100b51; BDUSS=lHU3ZqU2JhNDJqdnR6TGZqdkU3Um95cDdSQ2tSaUZiSUlkRWNjekczOUpBT0JhQVFBQUFBJCQAAAAAAAAAAAEAAAAJDRbOc2FkeXB5dGhvbmxrdAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElzuFpJc7hadH; TIEBAUID=48badcfee5e6ffd355f4b62d; bdshare_firstime=1522803027428; STOKEN=42c1109f07dd660e14ec447f5753e2cf85f174b779b852699cf778814a13486d; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; 3457551625_FRSVideoUploadTip=1; wise_device=0; BDSFRCVID=X3CsJeC62wWhRXb7WU-Q8zoXOe5c10QTH6ao5UoouSi9z5W9oqRYEG0PDM8g0KubbazpogKK0mOTHvbP; H_BDCLCKID_SF=tJPf_I0htIP3fPPkhDTJbb0hjmT22jnxt2neaJ5nJDoEex0Re5JN0M3-ya7E2hv95m0jBpLbQpP-HJ7zL4ub-lF7XJ5OhPrC5eTnKl0MLpbWbb0xynoD-l-wQfnMBMPjamOnaPQtLIFaMII6D5DaejPShMr2aK6KaI58LRu8Kb7VbIP6ebbkbfJBDlJfyhRDtbkjBtjvfPcooh73XR3xyj-7yajK2M60QnrG-T6Paq5BbDoxMDcpQT8rQ-FOK5OibCrpaC_Eab3vOIJzXpO154DreGLfq6-jJJC8VbOs2ROOKRj1MJrhhCCShUFsLJod-2Q-5KL-MI56EttGjT3nXU-JjJ5vX4ThBGA8afbdJJjoqUbbhRJ_Dx70MUJqQqcJ2gTxoUJgBCnJhhvG-ljzDCuebPRiJPr9Qgbq3ftLtD-bhDtxe5A35n-Wqlrt2t70KCo0QTrJabC3oKOJKU6qLT5X5nJ3QqvaJavPsxDyMJ7i8nKG-TL20q0njxQytlQya5TgBCTLJx0BDPj-WfonDh8vXH7MJUntKDrKXtJO5hvvhb6O3M7--lOh-p52f6_Dtn4e3e; H_PS_PSSID=26525_1422_26458_21092_18560_20881; PSINO=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1527410585,1527581980,1527582016,1527744276; __lnkrntdmcvrd=-1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1527744536',

        }
        self.kw = tieba
        self.dict_name = None
    # http请求
    def request_url(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    # 处理列表页的 详情页url和title
    def parse_url_data(self, res_byte):
        # html字符串转成element对象
        html = etree.HTML(res_byte)
        # element对象 xpath(xpath规则)解析
        a_list = html.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')
        # print(a_list)  # [<Element a at 0x1044c9a88>, <Element a at 0x1044c9a48>, <Element a at 0x1044c9a08>]

        for a_href in a_list:
            url_list = a_href.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a/@href')
            title_list = a_href.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a/text()')
        # print(url_list)  # ['/p/5690084419?fr=good', '/p/5631874883?fr=good', '/p/5584982730?fr=good']
        # print(title_list)  # ['【东立汉化】进击的巨人 第105话', '【东立汉化】进击的巨人 第104话', '【东立汉化】进击的巨人 第103话']
        return url_list,title_list

    def run(self):
        # 列表页地址
        url = self.url.format(self.kw)
        # 发出请求
        res_byte = self.request_url(url)
        # 返回列表页的 地址和title
        url_list, title_list = self.parse_url_data(res_byte)
        # 拼接完整详情页地址
        for detail_url in url_list:
            # 拼接文件夹的名字 = title
            self.dict_name = title_list[url_list.index(detail_url)]
            # 拼接完整地址
            detail_all_url = 'https://tieba.baidu.com' + detail_url
            # 发出请求
            detail_response = self.request_url(detail_all_url)
            # 处理详情页
            image_list = self.parse_detail_data(detail_response)
            # 保存图片
            self.loadimage(image_list,self.dict_name)
            # 还没翻页那

    def parse_detail_data(self, detail_response):
        html = etree.HTML(detail_response)
        image_list = html.xpath('//*[contains(@id,"post_content")]/img/@src')
        # print(image_list)  # ['https://imgsa.baidu.com/forum/w%3D580/sign=0af0979c8a18367aad897fd51e728b68/6127a61001e939019b9ed78b77ec54e734d196e1.jpg',]
        return image_list

    def loadimage(self, image_list,dir_name):
        if not os.path.exists('漫画/' + dir_name):
            # 创建相应文件夹
            os.makedirs('漫画/' + dir_name)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                # 'Host': 'tieba.baidu.com',
                'Cookie': 'BAIDUID=C95F4EB2802449AE1F812CC158E40C58:FG=1; BIDUPSID=C95F4EB2802449AE1F812CC158E40C58; PSTM=1520245998; TIEBA_USERTYPE=6f0cc0f466b909d65f100b51; BDUSS=lHU3ZqU2JhNDJqdnR6TGZqdkU3Um95cDdSQ2tSaUZiSUlkRWNjekczOUpBT0JhQVFBQUFBJCQAAAAAAAAAAAEAAAAJDRbOc2FkeXB5dGhvbmxrdAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElzuFpJc7hadH; TIEBAUID=48badcfee5e6ffd355f4b62d; bdshare_firstime=1522803027428; STOKEN=42c1109f07dd660e14ec447f5753e2cf85f174b779b852699cf778814a13486d; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; 3457551625_FRSVideoUploadTip=1; wise_device=0; BDSFRCVID=X3CsJeC62wWhRXb7WU-Q8zoXOe5c10QTH6ao5UoouSi9z5W9oqRYEG0PDM8g0KubbazpogKK0mOTHvbP; H_BDCLCKID_SF=tJPf_I0htIP3fPPkhDTJbb0hjmT22jnxt2neaJ5nJDoEex0Re5JN0M3-ya7E2hv95m0jBpLbQpP-HJ7zL4ub-lF7XJ5OhPrC5eTnKl0MLpbWbb0xynoD-l-wQfnMBMPjamOnaPQtLIFaMII6D5DaejPShMr2aK6KaI58LRu8Kb7VbIP6ebbkbfJBDlJfyhRDtbkjBtjvfPcooh73XR3xyj-7yajK2M60QnrG-T6Paq5BbDoxMDcpQT8rQ-FOK5OibCrpaC_Eab3vOIJzXpO154DreGLfq6-jJJC8VbOs2ROOKRj1MJrhhCCShUFsLJod-2Q-5KL-MI56EttGjT3nXU-JjJ5vX4ThBGA8afbdJJjoqUbbhRJ_Dx70MUJqQqcJ2gTxoUJgBCnJhhvG-ljzDCuebPRiJPr9Qgbq3ftLtD-bhDtxe5A35n-Wqlrt2t70KCo0QTrJabC3oKOJKU6qLT5X5nJ3QqvaJavPsxDyMJ7i8nKG-TL20q0njxQytlQya5TgBCTLJx0BDPj-WfonDh8vXH7MJUntKDrKXtJO5hvvhb6O3M7--lOh-p52f6_Dtn4e3e; H_PS_PSSID=26525_1422_26458_21092_18560_20881; PSINO=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1527410585,1527581980,1527582016,1527744276; __lnkrntdmcvrd=-1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1527744536',
                'Host': 'imgsa.baidu.com',

            }
            i = 0
            for detail_image_url in image_list:
                if '.jpg' in detail_image_url:
                    print(detail_image_url)
                    i += 1
                    image = requests.get(detail_image_url,headers=headers).content

                    print(image)
                    with open('漫画/' + dir_name + '/'  + str(i) + '.jpg' , 'wb') as f:
                        f.write(image)
                    # 详情页也没翻页那
            print('下载了%s页的图片' % i)
        else:
            print('当前文件夹的图片已经存在')



if __name__ == '__main__':
    tieba = input('请输入爬取图片的贴吧:')
    tiebaimage = tiebaDetailImage(tieba)
    tiebaimage.run()