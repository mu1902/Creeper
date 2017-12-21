''' 爬取沪深港通数据 '''
import datetime
import json

from pyquery import PyQuery as pq

import Creeper as cp

urls = ["http://sc.hkex.com.hk/TuniS/www.hkex.com.hk/chi/csm/DailyStat/",
        "http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk",
        "http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh",
        "http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz"
        ]
dn = datetime.date.today()
d = cp.tool.preDay(dn)


def parse_html1(content, _id=None):
    ''' 处理页面 '''
    res = []
    if content != "":
        data = json.loads(content.decode('utf-8').split(' = ')[1])
        for da in data:
            if da['market'] == 'SSE Northbound':
                typ = '沪股通'
            elif da['market'] == 'SSE Southbound':
                typ = '港股通沪'
            elif da['market'] == 'SZSE Northbound':
                typ = '深股通'
            elif da['market'] == 'SZSE Southbound':
                typ = '港股通深'
            else:
                typ = ''
            for row in da['content'][1]['table']['tr']:
                r = row['td'][0]
                if r[1] != '-':
                    r[1] = r[1] if len(r[1]) >= 5 else (
                        6 - len(r[1])) * '0' + r[1]
                    res.append({
                        "code": r[1],
                        # "name": r[2].replace('\u3000', ''),
                        "type": typ,
                        "date": d.strftime('%Y-%m-%d'),
                        "buy": int(r[3].replace(',', '')),
                        "sell": int(r[4].replace(',', ''))
                    })
    return res


def parse_html2(content, _id=None):
    ''' 处理页面 '''
    res = []
    if content != "":
        data = pq(content)(".result-table tr")
        __VIEWSTATE = pq(content)("#__VIEWSTATE").val()
        __VIEWSTATEGENERATOR = pq(content)("#__VIEWSTATEGENERATOR").val()
        __EVENTVALIDATION = pq(content)("#__EVENTVALIDATION").val()
        for tr in data:
            code = pq(tr)("td:eq(0)").text()
            if code:
                if len(code) <= 4:
                    code = (5 - len(code)) * '0' + code
                    typ = '港股通'
                elif code[0] == '9':
                    code = '60' + code[1:]
                    typ = '沪股通'
                elif code[0] == '7':
                    if code[0:2] == '70':
                        code = '000' + code[2:]
                    elif code[0:2] == '72':
                        code = '002' + code[2:]
                    elif code[0:2] == '77':
                        code = '300' + code[2:]
                    typ = '深股通'
                else:
                    typ = ''
                try:
                    res.append({
                        "code": code,
                        "type": typ,
                        "date": d.strftime('%Y-%m-%d'),
                        "volume": int(pq(tr)("td:eq(2)").text().replace(',', '')) if pq(tr)("td:eq(2)").text() else 0,
                        "proportion": float(pq(tr)("td:eq(3)").text()[:-1]) / 100 if pq(tr)("td:eq(3)").text() else 0
                    })
                except Exception as e:
                    print(e)
    return res


def HKEX():
    top = []
    change = []
    if not cp.tool.isHoliday(dn):
        t = datetime.datetime.now().timestamp()
        t_str = str(t * 1000)[0:13]
        param = 'data_tab_daily_' + d.strftime('%Y%m%d') + 'c.js?' + t_str
        html = cp.downloader.get_html(urls[0] + param, method='get')
        top = parse_html1(html)

    __VIEWSTATE = ''
    __VIEWSTATEGENERATOR = ''
    __EVENTVALIDATION = ''

    for i in range(3):
        if not cp.tool.isHoliday(dn):
            if __VIEWSTATE == '':
                html = cp.downloader.get_html(
                    urls[i + 1], {}, method='get').decode('utf-8')
            else:
                html = cp.downloader.get_html(urls[i + 1], {
                    "__VIEWSTATE": __VIEWSTATE,
                    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                    "__EVENTVALIDATION": __EVENTVALIDATION,
                    "ddlShareholdingDay": "0" * (2 - len(str(d.day))) + str(d.day),
                    "ddlShareholdingMonth": "0" * (2 - len(str(d.month))) + str(d.month),
                    "ddlShareholdingYear": str(d.year),
                    "btnSearch.x": "43",
                    "btnSearch.y": "8"}, method='post')
                if type(html) == bytes:
                    html = html.decode('utf-8')
            change.extend(parse_html2(html))
        __VIEWSTATE = ''

    print(top)
    print(change)
    # print("Top10: %d." % (cp.tool.to_mysql(top, 'creeper', 'hktop10')))
    # print("Proportion: %d." % (cp.tool.to_mysql(
    #     change, 'creeper', 'hkproportion')))


if __name__ == '__main__':
    HKEX()
