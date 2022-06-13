# -- coding: utf-8 --
"""
:authors:
    zhuxiaohu@baidu.com
:create_date:
    2022/6/10 6:24 下午
:last_date:
    2022/6/10 6:24 下午
:description:
    
"""
import requests


def fun(ip_port):
    result = False
    proxy = {"http": "http://" + ip_port}
    url = "http://www.baidu.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }
    response = requests.get(url, headers=headers, proxies=proxy)
    print response.content
    if "全球领先的中文搜索引擎" in response.content:
        result = True
    return result

if __name__ == "__main__":
    print "start check proxy"
    fun()