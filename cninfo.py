''' 爬取深交所互动易股东数回答 '''
import datetime
import json
import random
import re
import sys
import os.path

from pyquery import PyQuery as pq

import Creeper as cp


urls = {"sseinfo": "http://sns.sseinfo.com/ajax/feeds.do",
        "cninfo": "http://irm.cninfo.com.cn/ircs/index/search"}


def parse_sseinfo(content, _id=None):
    t = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d%H%M')
    if content != "":
        docs = pq(content)('.m_feed_txt a').items()
    else:
        return None
    res = []
    for d in docs:
        title = pq(d).text()
        url = pq(d).attr('href')
        time = os.path.split(url)[1][:12]
        if time > t:
            if re.search('投资者|调研', title) != None:
                res.append({'title': title, 'url': url})
        else:
            break
    return res


def parse_szseinfo(content, _id=None):
    t = (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
    if content != "":
        docs = json.loads(content)['results']
    else:
        return None
    res = []
    for d in docs:
        title = d['mainContent']
        url = 'http://static.cninfo.com.cn/' + \
            d['attachmentUrl'] if 'attachmentUrl' in d.keys() else ''
        time = d['pubDate']
        if int(time) > t*1000:
            if re.search('投资者|调研', title) != None:
                res.append({'title': title, 'url': url})
        else:
            break
    return res


def get_html():
    # 上交所
    # ran = random.random()
    # html_sse = cp.downloader.get_html(urls['sseinfo'], {'type': 30,
    #                                                     'pageSize': 50,
    #                                                     'lastid': -1,
    #                                                     'show': 1,
    #                                                     'page': 1,
    #                                                     '_': str(ran)}, method='get')
    # ir_sse = parse_sseinfo(html_sse)

    # 深交所
    html_szse = cp.downloader.get_html(urls['cninfo'], {'market': '',
                                                        'keyWord': '',
                                                        'industry': '',
                                                        'pageNo': 1,
                                                        'pageSize': 50,
                                                        'searchTypes': 4,
                                                        'stockCode': ''}, method='post', header={"Content-Type": "application/x-www-form-urlencoded"})
    ir_szse = parse_szseinfo(html_szse)


if __name__ == '__main__':
    get_html()
