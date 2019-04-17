''' 爬取沪深港通数据 '''
import datetime
import json
import random
import re

import Creeper as cp
from pyquery import PyQuery as pq

urls = {"sse": "http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm",
        "szse": "http://www.szse.cn/api/disc/announcement/annList"}
keywords = ['中标', '合同', '框架协议', '订单', '产品价格', '独立上市', '要约收购']


def parse_html_sse(content, _id=None):
    if content != "":
        data = pq(content)("dd")
    else:
        return None
    anct = [{'title': pq(dd)("em a").text(), 'url': pq(
        dd)("em a").attr('href')} for dd in data]
    anct = [a for a in anct if re.search(
        '|'.join(keywords), a['title']) != None]
    return anct


def parse_html_szse(content, _id=None):
    if content != "":
        data = json.loads(content)['data']
    else:
        return None
    anct = [{'title': d['title'],
             'url': 'http://www.szse.cn/disclosure/listed/bulletinDetail/index.html?'+d['id']} for d in data]
    anct = [a for a in anct if re.search(
        '|'.join(keywords), a['title']) != None]
    return anct


def get_html():
    html_sse = cp.downloader.get_html(urls['sse'], {}, method='post')
    anct_sse = parse_html_sse(html_sse)

    ran = random.random()
    html_szse = cp.downloader.get_html(
        urls['szse']+'?random='+str(ran),
        request_data=json.dumps({"channelCode": ["listedNotice_disc"],
                                 "pageNum": 1,
                                 "pageSize": 30,
                                 "seDate": ["2019-04-17", "2019-04-17"]}),
        method='post',
        header={"Content-Type": "application/json"})
    anct_szse = parse_html_szse(html_szse)

    message_s = [a['title'] + '\n' + a['url'] for a in anct_sse]
    message_sz = [a['title'] + '\n' + a['url'] for a in anct_szse]
    # print('\n'.join(message_s) + '\n' + '\n'.join(message_sz))
    cp.tool.send_email(['wangyf@xunlc.cn', 'zhongc@fundbj.com'], '交易所公告筛选', '\n'.join(
        message_s) + '\n' + '\n'.join(message_sz))


if __name__ == '__main__':
    get_html()
