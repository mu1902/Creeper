''' 爬取深交易股东数回答 '''
import datetime
import re
import sys

from pyquery import PyQuery as pq

import Creeper as cp


def parse_html(content):
    ''' 处理页面 '''
    code = pq(content)('.answer_Box .comCode a').items()
    name = pq(content)('.answer_Box .comName a').items()
    des = pq(content)('.answer_Box .answerBox .cntcolor').items()
    raw = zip(code, name, des)
    res = []
    for r in raw:
        if '股东' in r[2].text():
            n_pos = r[2].text().find('日')

            pattern_date = re.compile(r'(截.*日)')
            res_date = pattern_date.search(r[2].text())
            date = res_date.group(0) if res_date else ''

            pattern_number = re.compile(
                r'([0-9]+[,]*[0-9]*[.]?[0-9]*[人户万名，。]?)')
            res_number = pattern_number.search(r[2].text(), n_pos)
            num = res_number.group(0) if res_number else ''

            res.append((r[0].text(), r[1].text(), date, num))
    return res


if __name__ == '__main__':
    start = (datetime.date.today() -
             datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    end = datetime.date.today().strftime('%Y-%m-%d')
    key = '股东'
    # 参数从1开始
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
        for item in parse_html(cp.download.get_html(url, post_data)):
            res_list.append(item)
        cp.tool.progressbar(i + 1, 100)
    cp.tool.to_excel(res_list, 'shareholder')
