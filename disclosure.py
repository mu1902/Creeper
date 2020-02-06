''' 爬取港交易所权益披露数据 '''
import datetime

import Creeper as cp
from pyquery import PyQuery as pq

urls = {"hkex": "https://sc.hkexnews.hk/TuniS/di.hkex.com.hk/di/NSSrchCorpList.aspx"}
codes = ['0336', '0719', '1448']


def get_html():
    table = ''
    today = datetime.date.today().strftime('%d/%m/%Y')
    for c in codes:
        html = cp.downloader.get_html(
            urls['hkex'], {"sa1": "cl",
                        "src": "MAIN",
                        "lang": "ZH",
                        "scsd": today,
                        "sced": today,
                        "sc": c}, method='get')
        if html != "":
            detail_a = pq(html)("a:contains('所有披露权益通知')")
            for a in detail_a:
                # print(pq(a).attr("href"))
                u = pq(a).attr("href")
                html = cp.downloader.get_html(u, {}, method='get')
                if html != "":
                    if pq(html)("#lblRecCount").text() != "0":
                        table += pq(html)("#Table2").html()
                        table += pq(html)("#Table4 tr:eq(0)").html()
                # print(table)
    
    table = table if table != '' else '无'
    # cp.tool.send_email([], '持仓港股股权披露', table, 'html', 'utf')
    cp.tool.send_email(['wujg@xunlc.cn', 'zhongc@xunlc.cn',
                        'zhengy@xunlc.cn'], '持仓港股股权披露', table, 'html', 'utf')


if __name__ == '__main__':
    get_html()
