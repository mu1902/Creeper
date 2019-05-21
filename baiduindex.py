''' 爬取百度指数数据 '''
import datetime
import json

import js2py
import numpy as np

import Creeper as cp
import pandas as pd

urls = ['http://index.baidu.com/api/SearchApi/index',
        'http://index.baidu.com/Interface/ptbk']
today = datetime.date.today()
start = (today-datetime.timedelta(days=11)).strftime('%Y-%m-%d')
end = (today-datetime.timedelta(days=2)).strftime('%Y-%m-%d')
word = "曼联"


def get_data():
    index = cp.downloader.get_html(
        urls[0],
        request_data={"area": 0,
                      "word": word,
                      "startDate": start,
                      "endDate": end},
        method='get',
        header={"Cookie": "BAIDUID=F15D73EE05D782139EDBB3823E6C6926:FG=1; BIDUPSID=F15D73EE05D782139EDBB3823E6C6926; PSTM=1547104009; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1558332006; BDUSS=RuM1d4Tzc0b0R3aXNnVjV-MjBBLWtrN2RmfjZKSy1TWXdPflR5ZEJEdDd6d2xkSVFBQUFBJCQAAAAAAAAAAAEAAADJYpcHYXJ0ZW1pc18xODc3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHtC4lx7QuJcfn; CHKFORREG=c1d2821ba1126fc48d76a0dc2f7d86e6; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1558332028; bdindexid=2meer4i462jtpremkmv75f4ku6"})
    data = json.loads(index)
    return data


def get_key(data):
    key = cp.downloader.get_html(
        urls[1],
        request_data={"uniqid": data['data']['uniqid']},
        method='get',
        header={"Cookie": "BAIDUID=F15D73EE05D782139EDBB3823E6C6926:FG=1; BIDUPSID=F15D73EE05D782139EDBB3823E6C6926; PSTM=1547104009; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1558332006; BDUSS=RuM1d4Tzc0b0R3aXNnVjV-MjBBLWtrN2RmfjZKSy1TWXdPflR5ZEJEdDd6d2xkSVFBQUFBJCQAAAAAAAAAAAEAAADJYpcHYXJ0ZW1pc18xODc3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHtC4lx7QuJcfn; CHKFORREG=c1d2821ba1126fc48d76a0dc2f7d86e6; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1558332028; bdindexid=2meer4i462jtpremkmv75f4ku6"})
    data = json.loads(key)
    return data


def decrypt(key, data):
    decrypt = js2py.eval_js('''function(t, e) {
        for (var n = t.split(""), i = e.split(""), a = {}, r = [], o = 0; o < n.length / 2; o++)
            a[n[o]] = n[n.length / 2 + o];
        for (var s = 0; s < e.length; s++)
            r.push(a[i[s]]);
        return r.join("")
    }''')
    return decrypt(key, data)


def get_index():
    data = get_data()
    key = get_key(data)
    series = decrypt(key['data'], data['data']
                     ['userIndexes'][0]['all']['data'])

    df = pd.DataFrame({'date': pd.date_range(start, end),
                       'index': series.split(',')
                       })
    print(df)


if __name__ == '__main__':
    get_index()
