# -*- coding: utf-8 -*-
'''
modules
存放各种爬虫功能模板
后续如果数量多了, 可以进行抽象成类
'''

import urllib2
import socket
import logging
import re
from bs4 import BeautifulSoup

logger = logging.getLogger("spider.modules")

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
    proxy_handler = urllib2.ProxyHandler({"http": "http://192.168.59.242:44444"})
    null_proxy_handler = urllib2.ProxyHandler({})
    if proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)
    try:
        page = urllib2.urlopen(req)
        html = page.read()
        # html = html.decode("utf-8")
        return html.replace("\n", "")
    except urllib2.HTTPError, e:
        logger.error("爬取页面时发生错误 [%s] [http] %s" % (url, e))
    except urllib2.URLError, e:
        logger.error("爬取页面时发生错误 [%s] [url] %s" % (url, e))
    except socket.timeout, e:
        logger.error("爬取页面时超时 [%s] [socket] %s" % (url, e))


def get_my_blog(url, keyword, degree):
    logger.debug("抓取url: %s" % url)
    html = _scriping_html(url)
    res_dict = {
        "url": url,
        "keyword": keyword,
        "matched": False,
        "deep_url": []
    }
    if not html:
        logger.warn("页面抓取失败")
        return res_dict
    if keyword:
        key_regex = re.compile(keyword)
    else:
        key_regex = r"?.*"
    if degree == "simple":
        logger.debug("使用simple模式进行抓取页面")
        mat = re.match(key_regex, html)
        if mat:
            res_dict["matched"] = True
        return res_dict
    elif degree == "deep":
        logger.debug("使用deep模式进行抓取页面")
        soup = BeautifulSoup(html)
        key_str = soup.find(text=key_regex)
        if key_str:
            res_dict["matched"] = True
        a_tags = soup.find_all("a")
        for tag in a_tags:
            h = tag["href"]
            if re.match(url_regex, h):
                res_dict["deep_url"].append(h)
        return res_dict
    return res_dict
