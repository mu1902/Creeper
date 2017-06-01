''' 爬取同花顺龙虎榜 '''
import datetime
import re
import sys

from pyquery import PyQuery as pq

import Creeper as cp


def parse_html(content, _id):
    ''' 处理页面 '''
    stocks = pq(content).find('.rightcol .stockcont')
    res = []
    for t in stocks.items():
        title = t.children('p:first').text()
        date = _id
        code = title.split(')')[0][-6:]
        name = title.split('(')[0]
        reason = title.split('：')[1]

        table1 = t.find('tbody:eq(0) tr')
        for tr in table1.items():
            way = "最大买入"
            depart = tr.find('a').attr('title')
            vol = tr.children('td').eq(1).text()
            res.append((date, code, name, reason, way, depart, vol))
        table2 = t.find('tbody:eq(1) tr')
        for tr in table2.items():
            way = "最大卖出"
            depart = tr.find('a').attr('title')
            vol = tr.children('td').eq(2).text()
            res.append((date, code, name, reason, way, depart, vol))

    return res


if __name__ == '__main__':
    start = (datetime.date.today() -
             datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end = datetime.date.today().strftime('%Y-%m-%d')
    # 参数从1开始
    for i in range(1, len(sys.argv)):
        if i == 1:
            start = sys.argv[i]
        elif i == 2:
            end = sys.argv[i]
        else:
            pass

    url = 'http://data.10jqka.com.cn/ifmarket/lhbggxq/report/'
    res_list = []
    dalta = (datetime.datetime.strptime(end, '%Y-%m-%d') -
             datetime.datetime.strptime(start, '%Y-%m-%d')).days
    for i in range(dalta):
        date_str = (datetime.datetime.strptime(
            start, '%Y-%m-%d') + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        html = cp.downloader.get_html(url + date_str + '/').decode('GBK')
        res_list.extend(parse_html(html, date_str))
        cp.tool.progressbar(i + 1, dalta)
    cp.tool.to_excel(res_list, 'longhu')
    print(len(res_list))
