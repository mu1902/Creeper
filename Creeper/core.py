''' 爬虫核心类 '''
import datetime
import re
import sys
import urllib
from queue import Queue
from threading import Thread

from pyquery import PyQuery as pq

THREAD_NUM = 10


def get_html(url, post_data, link_sel=''):
    ''' 获取页面 '''
    req = urllib.request.Request(url)
    data = urllib.parse.urlencode(post_data).encode('utf-8')
    content = urllib.request.urlopen(req, data).read()
    doc = pq(content)
    return doc


def parse_html(pq, content_sel, link_sel=''):
    ''' 处理页面 '''
    fil = list(pq(content_sel).items())
    res = []
    for i in range(0, len(fil), 3):
        if '股东' in fil[i + 2].text():
            n_pos = fil[i + 2].text().find('截')
            date = ''
            if n_pos >= 0:
                date = fil[i + 2].text()[n_pos:n_pos + 12]
            pattern = re.compile(
                r'([一二三四五六七八九零十百千万亿]+|[0-9]+[,]*[0-9]+.[0-9]+[人户万名，。])')
            number = pattern.search(fil[i + 2].text(), n_pos + 12)
            num = number.group(0) if number else ''
            res.append((fil[i].text(), fil[i + 1].text(),
                        date, num))
    return res


if __name__ == '__main__':
    # q_job = Queue()
    # 参数从1开始
    start = (datetime.datetime.now() -
             datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    key = '股东'
    for i in range(1, len(sys.argv)):
        if i == 1:
            start = sys.argv[i]
        elif i == 2:
            end = sys.argv[i]
        elif i == 3:
            key = sys.argv[i]
        else:
            pass

    url = 'http://irm.cninfo.com.cn/ircs/interaction/topSearchForSzse.do'
    post_data = {
        'condition.dateFrom': start,
        'condition.dateTo': end,
        'condition.keyWord': key,
        'pageNo': 0,
        'pageSize': 10}
    for i in range(100):
        post_data['pageNo'] = i + 1
        r = parse_html(get_html(url, post_data),
                       '.answer_Box .comCode a, .comName a, .answerBox .cntcolor')
        for item in r:
            print(item)
