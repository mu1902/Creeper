''' 爬取交易所公告数据 '''
import datetime
import json
import os
import random
import re
import time
import sys

import Creeper as cp
from pyquery import PyQuery as pq
import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
from win32com.client import Dispatch
from pywintypes import com_error

DIR = os.path.dirname(os.path.abspath(__file__))

urls = {"sse": "http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm",
        "szse": "http://www.szse.cn/api/disc/announcement/annList",
        "hse": "https://www1.hkexnews.hk/ncms/json/eds/lcisehk1relsdc_1.json",
        "sseinfo": "http://sns.sseinfo.com/ajax/feeds.do",
        "cninfo": "http://irm.cninfo.com.cn/ircs/index/search"}
keywords = [['重组并购', '(重组|收购|购买|置换)((?!(报告书|公告书|修订)).)*摘要((?!(提示|进展|修订|补充)).)*$', '收购.*意向书'],
            ['分拆上市', '分拆.*上市'],
            ['大股东变更', '大股东变更'],
            ['要约收购', '要约收购报告书摘要'],
            ['回购增持', '(回购公司|增持)((?!(进展|意见|结果)).)*$'],
            ['增发', '发行(股份|A股).*预案'],
            ['变更公司名称', '变更.*公司名称', '变更.*证券简称'],
            ['董事会变更', '聘.*董事会秘书', '董事會秘書'],
            ['合同价格', '中标', '框架协议', '合同', '订单', '产品价格']]
codes = [[['wujg@xunlc.cn'], '00336', '01448'],
         [['zhongc@xunlc.cn'], '300741', '00336', '01448'],
         [['zhengy@xunlc.cn'], '300741', '00336', '01448'],
         [['wangyf@xunlc.cn'], '00336', '01448'],
         [['penglm@xunlc.cn'], '600114', '02382', '300285', '300750', '002812', '603659', '002850', '002460']]

n = datetime.datetime.now()
if n.hour < 12:
    day1 = datetime.date.today().strftime('%Y-%m-%d')
    day2 = day1
else:
    day1 = datetime.date.today().strftime('%Y-%m-%d')
    day2 = (datetime.date.today() +
            datetime.timedelta(days=1)).strftime('%Y-%m-%d')


def parse_html_sse(content, _id=None):
    if content != "":
        data = pq(content)("dd")
    else:
        return [], []
    anct = [{'title': pq(dd)("em a").text(), 'code': pq(dd).attr(
        'data-seecode'), 'url': pq(dd)("em a").attr('href')} for dd in data]
    res, res_c = [], []
    for k in keywords:
        res.append([a for a in anct if re.search(
            '|'.join(k[1:]), a['title']) != None])
    for c in codes:
        res_c.append([a for a in anct if a['code'] in c[1:]])
    return res, res_c


def parse_html_szse(content, _id=None):
    if content != "":
        data = json.loads(content)['data']
    else:
        return [], []
    anct = [{'title': d['title'], 'code': d['secCode'][0],
             'url': 'http://www.szse.cn/disclosure/listed/bulletinDetail/index.html?'+d['id']} for d in data]
    res, res_c = [], []
    for k in keywords:
        res.append([a for a in anct if re.search(
            '|'.join(k[1:]), a['title']) != None])
    for c in codes:
        res_c.append([a for a in anct if a['code'] in c[1:]])
    return res, res_c


def parse_html_hse(content, _id=None):
    if content != "":
        data = json.loads(content)['newsInfoLst']
    else:
        return [], []
    anct = [{'title': d['stock'][0]['sc'] + '-' + d['stock'][0]['sn'] + '-' + d['title'], 'code': d['stock'][0]['sc'],
             'url': 'https://www1.hkexnews.hk'+d['webPath']} for d in data]
    res, res_c = [], []
    for k in keywords:
        res.append([a for a in anct if re.search(
            '|'.join(k[1:]), a['title']) != None])
    for c in codes:
        res_c.append([a for a in anct if a['code'] in c[1:]])
    return res, res_c


def parse_sseinfo(content, _id=None):
    t = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d%H%M')
    if content != "":
        docs = pq(content)('.m_feed_txt a').items()
    else:
        return []
    res = []
    for d in docs:
        title = pq(d).text()
        url = pq(d).attr('href')
        time = os.path.split(url)[1][:12]
        if time > t:
            if re.search('投资者关系|调研活动', title) != None:
                res.append({'title': title, 'url': url})
        else:
            break
    return res


def parse_szseinfo(content, _id=None):
    t = (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
    if content != "":
        docs = json.loads(content)['results']
    else:
        return []
    res = []
    for d in docs:
        title = d['mainContent']
        url = 'http://static.cninfo.com.cn/' + \
            d['attachmentUrl'] if 'attachmentUrl' in d.keys() else ''
        time = d['pubDate']
        if int(time) > t*1000:
            if re.search('投资者关系|调研活动', title) != None:
                res.append({'title': title, 'url': url})
        else:
            break
    return res


def analysis_research_report(url):
    file_name = os.path.split(url)[-1]
    file_ext = file_name.split('.')[-1]
    # file_url = os.getcwd() + '\\tmp\\' + file_name
    file_url = DIR + '\\tmp\\' + file_name
    f = cp.downloader.get_file(url, file_url)
    if file_ext == 'doc' or file_ext == 'docx':
        try:
            word = Dispatch('Word.Application')
            doc = word.Documents.Open(file_url)
            file_name += ".pdf"
            file_ext = 'pdf'
            file_url += ".pdf"
            doc.SaveAs(file_url, FileFormat=17)
            doc.Close()
            word.Quit()
            time.sleep(3)
        except com_error as e:
            print(e)

    if file_ext == 'pdf':
        try:
            with pdfplumber.open(file_url) as f_pdf:
                pages = len(f_pdf.pages)
                address = ''
                # text = page.extract_text()
                # print(text)
                for p in f_pdf.pages:
                    tables = p.extract_tables()
                    if len(tables) > 0:
                        for tr in tables[0]:
                            # print(tr)
                            if tr[0] and '地点' in tr[0]:
                                address = tr[1] if tr[1] else ''
                                break
                    if address != '':
                        break
        except PDFSyntaxError:
            pages = 0
            address = ''
        return pages, address
    else:
        return 0, ''


def get_html():
    # 上交所
    html_sse = cp.downloader.get_html(urls['sse'], {}, method='post')
    anct_sse, anct_sse_c = parse_html_sse(html_sse)

    # 深交所
    ran = random.random()
    html_szse = cp.downloader.get_html(
        urls['szse']+'?random='+str(ran),
        request_data=json.dumps({"channelCode": ["listedNotice_disc"],
                                 "pageNum": 1,
                                 "pageSize": 30,
                                 "seDate": [day1, day2]}),
        method='post',
        header={"Content-Type": "application/json"})
    anct_szse, anct_szse_c = parse_html_szse(html_szse)

    num = int(json.loads(html_szse)['announceCount'] / 30) + 1
    print(num)
    for i in range(2, num+1):
        html_szse = cp.downloader.get_html(
            urls['szse']+'?random='+str(ran),
            request_data=json.dumps({"channelCode": ["listedNotice_disc"],
                                     "pageNum": i,
                                     "pageSize": 30,
                                     "seDate": [day1, day2]}),
            method='post',
            header={"Content-Type": "application/json"})
        if html_szse:
            html_szse_page, html_szse_page_c = parse_html_szse(html_szse)
            for i in range(len(keywords)):
                anct_szse[i].extend(html_szse_page[i])
            for i in range(len(codes)):
                anct_szse_c[i].extend(html_szse_page_c[i])
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
    anct_hse, anct_hse_c = parse_html_hse(html_hse)
    if anct_hse != None:
        print(len(anct_hse))

    # 上交所互动易
    ran = random.random()
    html_sse_info = cp.downloader.get_html(urls['sseinfo'], {'type': 30,
                                                             'pageSize': 50,
                                                             'lastid': -1,
                                                             'show': 1,
                                                             'page': 1,
                                                             '_': str(ran)}, method='get')
    ir_sse = parse_sseinfo(html_sse_info)

    # 深交所互动易
    html_szse_info = cp.downloader.get_html(urls['cninfo'], {'market': '',
                                                             'keyWord': '',
                                                             'industry': '',
                                                             'pageNo': 1,
                                                             'pageSize': 50,
                                                             'searchTypes': 4,
                                                             'stockCode': ''}, method='post', header={"Content-Type": "application/x-www-form-urlencoded"})
    ir_szse = parse_szseinfo(html_szse_info)

    message_all = ''
    message_favorite = []
    # 投资者关系
    ir = ir_sse + ir_szse
    message_all += '#组别1：投资者关系--关键词：投资者关系|调研活动--报告数：' + \
        str(len(ir)) + '\n'
    for a in ir:
        pages, address = analysis_research_report(a['url'])
        message_all += a['title'] + '【页数：' + str(pages) + \
            '】【地点：' + address + '】\n' + a['url'] + '\n'
    message_all += '\n'

    # 清空临时文件
    ls = os.listdir(DIR + '\\tmp\\')
    for i in ls:
        os.remove(os.path.join(DIR + '\\tmp\\', i))

    # 分组关键字
    for i in range(len(keywords)):
        count = len(anct_sse[i]) + len(anct_szse[i]) + len(anct_hse[i])
        kws = '|'.join(keywords[i][1:])
        kws = re.sub('\?\!', '-', kws)
        kws = re.sub('(\.|\$)', '', kws)
        message_all += '#组别' + str(i+2) + '：' + \
            keywords[i][0] + '--关键词：' + kws + '--报告数：' + str(count) + '\n'
        message_s = [a['title'] + '\n' + a['url'] + '\n' for a in anct_sse[i]]
        message_sz = [a['code'] + a['title'] + '\n' +
                      a['url'] + '\n' for a in anct_szse[i]]
        message_h = '' if anct_hse == None else [
            a['title'] + '\n' + a['url'] + '\n' for a in anct_hse[i]]
        message_all += ''.join(message_s) + \
            ''.join(message_sz) + ''.join(message_h) + '\n'

    # 关注股票清单
    for i in range(len(codes)):
        count = len(anct_sse_c[i]) + len(anct_szse_c[i]) + len(anct_hse_c[i])
        if count == 0:
            message_favorite.append('无')
        else:
            message_favorite_s = [a['title'] + '\n' +
                                  a['url'] + '\n' for a in anct_sse_c[i]]
            message_favorite_sz = [a['code'] + a['title'] +
                                   '\n' + a['url'] + '\n' for a in anct_szse_c[i]]
            message_favorite_h = [a['title'] + '\n' +
                                  a['url'] + '\n' for a in anct_hse_c[i]]
            message_favorite.append(''.join(message_favorite_s) +
                                    ''.join(message_favorite_sz) + ''.join(message_favorite_h) + '\n')

    # print(message_favorite)
    message_all = re.sub('(\u2022)+?', '', message_all)
    # cp.tool.send_email([], '交易所公告筛选', message_all)

    if n.hour < 12:
        cp.tool.send_email(['wangyf@xunlc.cn', 'penglm@xunlc.cn', 'wujg@xunlc.cn',
                            'zhongc@xunlc.cn', 'zhengy@xunlc.cn'], '交易所公告筛选', message_all)
        for i in range(len(codes)):
            if message_favorite[i] == '无':
                cp.tool.send_email(
                    [], '关注公司公告'+';'.join(codes[i][0]), message_favorite[i])
            else:
                cp.tool.send_email(codes[i][0], '关注公司公告', message_favorite[i])
    else:
        cp.tool.send_email(['wangyf@xunlc.cn', 'penglm@xunlc.cn',
                            'zhongc@xunlc.cn', 'zhengy@xunlc.cn'], '交易所公告筛选', message_all)
        for i in range(len(codes)):
            if i == 0:
                continue
            if message_favorite[i] == '无':
                cp.tool.send_email(
                    [], '关注公司公告'+';'.join(codes[i][0]), message_favorite[i])
            else:
                cp.tool.send_email(codes[i][0], '关注公司公告', message_favorite[i])


if __name__ == '__main__':
    get_html()
