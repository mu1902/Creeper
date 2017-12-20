''' 爬取新股数据 '''
import datetime
import json
import re
import sys

from pyquery import PyQuery as pq

import Creeper as cp


def parse_html(content):
    ''' 处理页面 '''
    if content:
        # print(type(content))
        content = content.decode('utf-8')
        res = []
        row = json.loads(content.split('=')[1][15:-1])
        for r in row:
            res.append((r['securitycode'], r['securityshortname'], r['sl']))
        return res


if __name__ == '__main__':
    url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get'
    post_data = {
        "type": "XGSG_LB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "st": "purchasedate,securitycode",
        "sr": -1,
        "p": 1,
        "ps": 50,
        "js": "var rXGpbPDJ={pages:(tp),data:(x)}",
        "rt": 50457704}
    res_list = []
    for i in range(36):
        post_data['p'] = i + 1
        res_list.extend(parse_html(
            cp.downloader.get_html(url, post_data)))
        cp.tool.progressbar(i + 1, 36)
    cp.tool.to_excel(res_list, 'newstock')
    print(len(res_list))
