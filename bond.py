''' 爬取可转债&可换债 '''
import datetime
import json
import re
import sys

from pyquery import PyQuery as pq

import Creeper as cp


def parse_html(content, _id):
    ''' 处理页面 '''
    res = []
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

    res_list = []
    url1 = 'http://query.sse.com.cn/infodisplay/queryBulletinKzzTipsNew.do?'
    sh_res1 = cp.downloader.get_html(url1,
                                     {"beginDate": start,
                                      "endDate": datetime.date.today().strftime('%Y-%m-%d'),
                                      "pageHelp.pageSize": 1000},
                                     'get',
                                     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
                                         "Host": "query.sse.com.cn",
                                         "Referer": "http://www.sse.com.cn/disclosure/bond/announcement/convertible/"}
                                     ).decode('UTF-8')
    sh_items1 = json.loads(sh_res1)["result"]
    for i in sh_items1:
        res_list.append((i["security_Code"], i["SSEDate"], i["title"], "沪市可转债"))

    url2 = 'http://query.sse.com.cn/commonSoaQuery.do?'
    sh_res2 = cp.downloader.get_html(url2,
                                     {"channelId": "9868", "sqlId": "BS_GGLL", "siteId": "28", "extGGLX": "11",
                                      "createTime": start + " 00:00:00",
                                      "createTimeEnd": datetime.date.today().strftime('%Y-%m-%d') + " 23:59:59"},
                                     'get',
                                     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
                                         "Host": "query.sse.com.cn",
                                         "Referer": "http://www.sse.com.cn/disclosure/bond/announcement/exchangeable/"}
                                     ).decode('UTF-8')
    sh_items2 = json.loads(sh_res2)["result"]
    for i in sh_items2:
        res_list.append(
            (i["stockcode"], i["createTime"], i["docTitle"], "沪市可交债"))

    url3 = 'http://disclosure.szse.cn/m/search0425.jsp'

    day1 = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    day2 = datetime.date.today()
    days = (day2 - day1).days

    for d in range(0, days, 60):
        sz_res1 = cp.downloader.get_html(url3,
                                         {"noticeType": "0109",
                                          "startTime": (day1 + datetime.timedelta(days=d)).strftime('%Y-%m-%d'),
                                          "endTime": (day1 + datetime.timedelta(days=(d + 59))).strftime('%Y-%m-%d'),
                                          "pageNo": 1}).decode('GB2312')
        sz_items1 = pq(sz_res1)('.td2 a').items()  # <a href="PDF相对地址">公告名称</a>
        for i in sz_items1:
            res_list.append((i.text().split('：')[0], i.attr(
                "href").split('/')[1], i.text().split('：')[1], "深市"))

        for i in range(int(pq(sz_res1)('.page12 span').eq(1).text()) + 1):
            if i > 1:
                sz_res1 = cp.downloader.get_html(url3,
                                                 {"noticeType": "0109",
                                                  "startTime": (day1 + datetime.timedelta(days=d)).strftime('%Y-%m-%d'),
                                                  "endTime": (day1 + datetime.timedelta(days=(d + 59))).strftime('%Y-%m-%d'),
                                                  "pageNo": i}).decode('GB2312')
                # <a href="PDF相对地址">公告名称</a>
                sz_items1 = pq(sz_res1)('.td2 a').items()
                for i in sz_items1:
                    res_list.append((i.text().split('：')[0], i.attr(
                        "href").split('/')[1], i.text().split('：')[1], "深市"))

    cp.tool.to_excel(res_list, 'bond')
    print(len(res_list))
