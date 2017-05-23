''' 爬虫核心类 '''
import datetime
import math
import re
import sys
import urllib
from queue import Queue
from threading import Thread

import xlwt
from pyquery import PyQuery as pq

THREAD_NUM = 10


def get_html(url, post_data, link_sel=''):
    ''' 获取页面 '''
    req = urllib.request.Request(url)
    data = urllib.parse.urlencode(post_data).encode('utf-8')
    con = urllib.request.urlopen(req, data).read()
    return con


def parse_html(content, link_sel=''):
    ''' 处理页面 '''
    fil = list(
        pq(content)('.answer_Box .comCode a, .comName a, .answerBox .cntcolor').items())
    res = []
    for i in range(0, len(fil), 3):
        if '股东' in fil[i + 2].text():
            n_pos = fil[i + 2].text().find('日')

            pattern_date = re.compile(r'(截.*日)')
            res_date = pattern_date.search(fil[i + 2].text())
            date = res_date.group(0) if res_date else ''

            pattern_number = re.compile(
                r'([0-9]+[,]*[0-9]*[.]?[0-9]*[人户万名，。]?)')
            res_number = pattern_number.search(fil[i + 2].text(), n_pos)
            num = res_number.group(0) if res_number else ''

            res.append((fil[i].text(), fil[i + 1].text(),
                        date, num))
    return res


def to_excel(res_list):
    excel = xlwt.Workbook()
    sheet = excel.add_sheet("my_sheet")
    for row in range(0, len(res_list)):
        for col in range(0, len(res_list[row])):
            sheet.write(row, col, res_list[row][col])
    excel.save("data.xls")


def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)),
                                     percent))
    sys.stdout.flush()


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
    res_list = []
    for i in range(100):
        post_data['pageNo'] = i + 1
        for item in parse_html(get_html(url, post_data)):
            res_list.append(item)
        progressbar(i + 1, 100)
    # print(res_list)
    to_excel(res_list)
    print('\nDone')
