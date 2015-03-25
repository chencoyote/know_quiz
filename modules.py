# -*- coding: utf-8 -*-
'''
modules
存放各种爬虫功能模板
后续如果数量多了, 可以进行抽象成类
'''


import urllib2
import socket
import re
from data import SpiderData
from bs4 import BeautifulSoup

sd = SpiderData()

url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def _scriping_html(url, proxy=True):
    socket.setdefaulttimeout(5)
    req = urllib2.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5")
    req.add_header("Accept", "text/html,*/*")
    if proxy:
        proxy_handler = urllib2.ProxyHandler({"http": "http://192.168.59.242:44444"})
    else:
        proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    try:
        page = urllib2.urlopen(req)
        html = page.read()
        return html
    except urllib2.HTTPError, e:
        print str(e)
    except urllib2.URLError, e:
        print "Error Reason:", e.reason
    except socket.timeout, e:
        print "Error Reason:", str(e)


def get_my_blog(url, keyword, degree):
    html = _scriping_html(url)
    res_dict = {
        "url": url,
        "keyword": keyword,
        "html": "",
        "deep_url": []
    }
    if not html:
        return res_dict
    if keyword:
        key_regex = re.compile(keyword)
    else:
        key_regex = r"?.*"
    if degree == "simple":
        mat = re.match(key_regex, html)
        if mat:
            res_dict["html"] = html
        return res_dict
    elif degree == "deep":
        soup = BeautifulSoup(html)
        key_str = soup.find(text=keyword)
        if key_str:
            res_dict["html"] = key_str
        a_tags = soup.find_all("a")
        for tag in a_tags:
            h = tag["href"]
            if re.match(url_regex, h):
                res_dict["deep_url"].append(h)
        return res_dict
    return res_dict
