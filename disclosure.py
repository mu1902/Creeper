''' 爬取港交易所权益披露数据 '''
import datetime

import Creeper as cp
from pyquery import PyQuery as pq

urls = {"hkex": "https://sc.hkexnews.hk/TuniS/di.hkex.com.hk/di/NSSrchCorpList.aspx"}
codes = ['0336', '1448']


def get_html():
    table = ''
    yesterday = (datetime.date.today() -
                 datetime.timedelta(days=1)).strftime('%d/%m/%Y')
    today = datetime.date.today().strftime('%d/%m/%Y')
    for c in codes:
        html = cp.downloader.get_html(
            urls['hkex'], {"sa1": "cl",
                           "src": "MAIN",
                           "lang": "ZH",
                           "scsd": yesterday,
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
                        table += c + "\n"
                        table += "*注解：(L) - 好仓,(S) - 淡仓,(P) - 可供借出的股份\n"
                        # table += pq(html)("#Table4 tr:eq(0)").html()
                        table += "人员名称 | 股份数目 | 平均价 | 持有股份数目 | 占比% | \n"
                        for tr in pq(html)("#grdPaging tr:gt(0)"):
                            for i in range(1, 7):
                                if i == 2:
                                    continue
                                table += pq(tr)("td:eq(" + str(i) +
                                                ")").text() + ' | '
                            table += '\n'
                # print(table)

    table = table if table != '' else '无'
    # charType = 'utf' if table != '无' else 'gbk'
    # msgType = 'html' if table != '无' else 'plain'
    # cp.tool.send_email([], '持仓港股股权披露', table)
    if table == '无':
        cp.tool.send_email([], '持仓港股股权披露', table)
    else:
        cp.tool.send_email(['wujg@xunlc.cn', 'zhongc@xunlc.cn',
                            'zhengy@xunlc.cn'], '持仓港股股权披露', table)


if __name__ == '__main__':
    get_html()
