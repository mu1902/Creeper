''' 爬取交易所公告数据 '''
import datetime
import json
import random
import re
import time
import sys

import Creeper as cp
from pyquery import PyQuery as pq

urls = {"sse": "http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm",
        "szse": "http://www.szse.cn/api/disc/announcement/annList",
        "hse": "https://www1.hkexnews.hk/ncms/json/eds/lcisehk1relsdc_1.json"}
keywords = [['中标', '合同', '框架协议', '订单', '产品价格'],
            ['董事会秘书', '证券事务代表', '董事會秘書', '證券事務代表'],
            ['独立上市', '要约收购'],
            ['搬迁', '关停', '爆炸', '事故']]
today = datetime.date.today().strftime('%Y-%m-%d')


def parse_html_sse(content, _id=None):
    if content != "":
        data = pq(content)("dd")
    else:
        return None
    anct = [{'title': pq(dd)("em a").text(), 'url': pq(
        dd)("em a").attr('href')} for dd in data]
    res = []
    for k in keywords:
        res.append([a for a in anct if re.search(
            '|'.join(k), a['title']) != None])
    return res


def parse_html_szse(content, _id=None):
    if content != "":
        data = json.loads(content)['data']
    else:
        return None
    anct = [{'title': d['title'],
             'url': 'http://www.szse.cn/disclosure/listed/bulletinDetail/index.html?'+d['id']} for d in data]
    res = []
    for k in keywords:
        res.append([a for a in anct if re.search(
            '|'.join(k), a['title']) != None])
    return res


def parse_html_hse(content, _id=None):
    if content != "":
        data = json.loads(content)['newsInfoLst']
    else:
        return None
    anct = [{'title': d['stock'][0]['sc'] + '-' + d['stock'][0]['sn'] + '-' + d['title'],
             'url': 'https://www1.hkexnews.hk'+d['webPath']} for d in data]
    res = []
    for k in keywords:
        res.append([a for a in anct if re.search(
            '|'.join(k), a['title']) != None])
    return res


def get_html():
    # 上交所
    html_sse = cp.downloader.get_html(urls['sse'], {}, method='post')
    anct_sse = parse_html_sse(html_sse)

    # 深交所
    ran = random.random()
    html_szse = cp.downloader.get_html(
        urls['szse']+'?random='+str(ran),
        request_data=json.dumps({"channelCode": ["listedNotice_disc"],
                                 "pageNum": 1,
                                 "pageSize": 30,
                                 "seDate": [today, today]}),
        method='post',
        header={"Content-Type": "application/json"})
    anct_szse = parse_html_szse(html_szse)

    num = int(json.loads(html_szse)['announceCount'] / 30) + 1
    print(num)
    for i in range(2, num+1):
        html_szse = cp.downloader.get_html(
            urls['szse']+'?random='+str(ran),
            request_data=json.dumps({"channelCode": ["listedNotice_disc"],
                                     "pageNum": i,
                                     "pageSize": 30,
                                     "seDate": [today, today]}),
            method='post',
            header={"Content-Type": "application/json"})
        if html_szse:
            html_szse_page = parse_html_szse(html_szse)
            for i in range(len(keywords)):
                anct_szse[i].extend(html_szse_page[i])
        else:
            print(i)
        if i % 20 == 0:
            time.sleep(1)
        else:
            time.sleep(0.1)

    # 港交所
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    html_hse = cp.downloader.get_html(
        urls['hse']+'?_='+str(int(timestamp*1000)), {}, method='get', header={"Content-Type": "application/json"})
    anct_hse = parse_html_hse(html_hse)

    message_all = ''
    for i in range(len(keywords)):
        message_all += '#关键词组：' + '|'.join(keywords[i])+'\n'
        message_s = [a['title'] + '\n' + a['url'] for a in anct_sse[i]]
        message_sz = [a['title'] + '\n' + a['url'] for a in anct_szse[i]]
        message_h = '' if anct_hse == None else [a['title'] + '\n' + a['url'] for a in anct_hse[i]]
        message_all += '\n'.join(message_s) + '\n' + \
            '\n'.join(message_sz) + '\n' + '\n'.join(message_h) + '\n\n'

    # print(message_all)
    # cp.tool.send_email([], '交易所公告筛选', message_all)
    cp.tool.send_email(['wangyf@xunlc.cn', 'xuex@xunlc.cn', 'penglm@xunlc.cn', 'zhongc@fundbj.com',
                        'xiezy@fundbj.com'], '交易所公告筛选', message_all)


if __name__ == '__main__':
    get_html()
