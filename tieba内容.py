import requests


def loadcontent(name, page_start, page_stop):
    start = int(page_start)
    stop = int(page_stop)
    while True:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        url = 'http://tieba.baidu.com/f'
        pn = (start - 1) * 50
        keys = {
            'kw' : name,
            'pn' : pn
        }
        response = requests.get(url,params=keys,headers=headers)
        html_bytes = response.content
        with open('tieba/' + name + '-' + str(start) + '.html','wb') as file:
            file.write(html_bytes)
        if start < stop:
            start += 1
        else:
            break

def run():
    name = input('请输入要爬取内容的贴吧名字:')
    page_start = input('开始的页数:')
    page_stop = input('结束的页数:')
    loadcontent(name,page_start,page_stop)


if __name__ == '__main__':
    # 指定爬取贴吧,指定页数,但是图片可能是内链接,失效了
    run()