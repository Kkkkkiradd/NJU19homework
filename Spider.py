import requests
import json
import time
from lxml import etree
import html
import re
from bs4 import BeautifulSoup


# encoding=utf-8
class Weibospider:
    def __init__(self):
        self.start_url = 'https://weibo.com/rmrb?is_all=1&stat_date=202006#feedtop'
        self.headers = {
            "accept": "textml,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "",
            "referer": "https://weibo.com/rmrb?is_all=1&stat_date=202001",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        }

    def parse_home_url(self, url):
        res = requests.get(url, headers=self.headers)
        response = res.content.decode('utf-8', 'ignore').replace("\\", "")
        print(response)
        every_id = re.compile('name=(\d+)', re.S).findall(response)
        home_url = []
        for id in every_id:
            base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&from=singleWeiBo'
            url = base_url.format(id)
            home_url.append(url)
        return home_url

    def parse_comment_info(self, url):
        res = requests.get(url, headers=self.headers)
        response = res.json()
        count = response['data']['count']
        html = etree.HTML(response['data']['html'])
        text = html.xpath("//div[@class='WB_detail']/text()")  # 微博正文
        info = html.xpath("//div[@node-type='replywrap']/div[@class='WB_text']/text()")  # 评论信息
        info = "".join(info).replace(" ", "").split("\n")
        info.pop(0)
        comment_time = html.xpath("//div[@class='WB_from S_txt2']/text()")  # 评论时间
        comment_info_list = []
        item = {}
        item["main_body"] = text  # 存储微博正文
        comment_info_list.append(item)
        for i in range(len(info)):
            item = {}
            item["comment_info"] = info[i]  # 存储评论的信息
            item["comment_time"] = comment_time[i]  # 存储评论时间
            comment_info_list.append(item)
        return count, comment_info_list

    def write_file(self, path_name, content_list):
        for content in content_list:
            with open(path_name, "a", encoding="UTF-8") as f:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")

    def run(self, path_name, n):
        start_url = 'https://weibo.com/rmrb?is_all=1&stat_date=202006&page={}#feedtop'
        for i in range(n):
            home_url = self.parse_home_url(start_url.format(i + 1))
            all_url = home_url
            print(all_url[0])
            all_count, comment_info_list = self.parse_comment_info(all_url[0])
            self.write_file(path_name, comment_info_list)
            comment_url = all_url[0]
            print(comment_url)
            time.sleep(0.2)


if __name__ == '__main__':
    path_name = "2020年7月微博评论.txt"
    weibo = Weibospider()
    weibo.run(path_name, 37)
