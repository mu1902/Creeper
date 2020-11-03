import datetime as dt
import json
import os
import re
import time

from pysqlcipher3 import dbapi2 as sqlite
import Creeper as cp
from pyquery import PyQuery as pq

date = dt.date.today() - dt.timedelta(days=7)
t_text = date.strftime('%Y-%m-%d')
t_num = int(time.mktime(date.timetuple())) * 1000


# 公众号
# 东方烟草报、HNB咨询与交流
def mp():
    os.system('nox_adb pull /data/data/com.tencent.mm/MicroMsg/87c8969adadf852b441173a366e2be9e/EnMicroMsg.db D:\Files\Wechat')

    PWD = '9c22ae0'
    DB_PATH = 'D:\Files\Wechat\EnMicroMsg.db'

    sql = '''
    select m.createTime, m.content, c.nickname
    from message as m, rcontact as c
    where m.type=285212721
    and c.nickname in ("东方烟草报","HNB咨询与交流")
    and m.talkerId=c.rowid
    and m.createTime>{0};
    '''.format(t_num)

    conn = sqlite.connect(DB_PATH)
    curs = conn.cursor()
    curs.execute("PRAGMA key='" + PWD + "';")
    curs.execute("PRAGMA kdf_iter = '4000';")
    curs.execute("PRAGMA cipher_use_hmac = OFF;")
    curs.execute(sql)

    message = ''
    for row in curs:
        message += row[2] + '\n'
        rawtxt = re.sub('([\x00-\x10]|\xd0)+?', '', row[1])
        count_str_arr = re.findall('\$count(\d+?)', rawtxt, re.S)
        count = int(count_str_arr[0]) if len(count_str_arr) > 0 else 0
        for i in range(count):
            c = str(i) if i > 0 else ''
            title = re.findall('item' + c + '\.title(.+?)\.msg', rawtxt, re.S)
            url = re.findall('item' + c + '\.url(.+?)&chksm=', rawtxt, re.S)
            message += title[0] + '\n' + url[0] + '\n'
        message += '\n'

    conn.close()
    return message
    # print(message)

# 网站
# 烟草在线


def ws_1():
    html = cp.downloader.get_html(
        "http://www.tobaccochina.com/xinxingyancao/index.shtml", method='get', code='gbk')
    data = pq(html)("div.change_show div.news_list ul.dc li")
    res = []
    for li in data:
        date = pq(li)('span').text()
        a = pq(li)('a').attr('href')
        title = pq(li)('a').text()
        if date < t_text:
            break
        else:
            res.append((title, date, a,))
    return res

# 网站
# 看研报


def kyb():
    cookies = cp.downloader.get_html(
        "https://www.kanzhiqiu.com/user/login.htm",
        request_data={
            "signonForwardAction": "",
            "login_submit": 1,
            "newlogin": "",
            "username": "19921239256",
            "password": "kyb2020",
            "j_captcha_response": "",
            "remember_name": 1
        },
        method="post",
        header={
            "Host": "www.kanzhiqiu.com",
            "Origin": "https://www.kanzhiqiu.com",
            "Referer": "https://www.kanzhiqiu.com/user/login.htm",
            "Connection": "keep-alive",
            "Content-Length": "119",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.56",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": "",
        },
        ret_cookies=True)
    # print(cookies)
    html = cp.downloader.get_html(
        "https://www.kanzhiqiu.com/newsadapter/fulltextsearch/fulltext_report_news_search.json",
        request_data={
            'starttime': '',
            'endtime': '',
            'page': 1,
            'pageSize': 20,
            'search': '烟草',
            'notSearch': '',
            'doccolumns': '',
            'doctypes': '',
            'industrycodes': '',
            'brokers': '',
            'stkcodes': '',
            'analystIds': '',
            'searchSaveId': '',
            'pageNumStart': '',
            'mystock': '',
            'sortByPagenum': False,
            'sortByHot': False,
            'sortByTime': True,
            'investrank': '',
            'industryrank': '',
            'marketOC': False,
            'marketKCB': False,
            'language': '',
            'clickFrom': 0,
            'hyperSearchField': 'title',
            'j_captcha_response': '',
            'newsPageSize': 25,
            'newsDealSpecialDocColumn': True,
            'timeOut': 200
        },
        method='post',
        cookie=cookies)

    data = json.loads(html)['reports']['reports']
    res = []
    for rpt in data:
        title = rpt['title']
        author = rpt['author']
        a = 'https://www.kanzhiqiu.com/newreport/detail.htm?docid=' + rpt['id']
        date = rpt['createat']
        if date < t_num:
            break
        else:
            res.append((title, author, date, a,))
    return res


if __name__ == '__main__':
    # print(mp())
    # print(ws_1())
    print(kyb())
    # cp.tool.send_email([], '报告', message)
