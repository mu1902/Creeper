import json
import random
import pandas as pd

import Creeper as cp
from pyquery import PyQuery as pq

ran = random.random()
html = cp.downloader.get_html('http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.15669350475330956&page=0&size=300',
                              request_data=json.dumps(
                                  {'establishDate': {'from': "2019-02-10", 'to': "2020-02-10"}}),
                              method='post',
                              header={"Content-Type": "application/json"})
data = json.loads(html)['content']

rows = []
for d in data:
    row = [d['managerName'], d['artificialPersonName'], d['primaryInvestType'],
           d['registerProvince'], d['registerNo'], d['establishDate']/1000, d['registerDate']/1000]
    detail_html = cp.downloader.get_html(
        'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/'+d['url'], method='get')
    allPerson = pq(detail_html)(
        "div.info-body div:nth-child(2) div:nth-child(2) table tbody tr:nth-child(15) td:nth-child(2)").text()
    passPerson = pq(detail_html)(
        "div.info-body div:nth-child(2) div:nth-child(2) table tbody tr:nth-child(16) td:nth-child(2)").text()
    lawFirm = pq(detail_html)(
        "div.info-body div:nth-child(4) div:nth-child(2) table tbody td:nth-child(3)").text()
    lawyer = pq(detail_html)(
        "div.info-body div:nth-child(4) div:nth-child(2) table tbody td:nth-child(5)").text()
    row.extend((allPerson, passPerson, lawFirm, lawyer,))
    rows.append(row)

# print(rows)

df = pd.DataFrame(rows, columns=['私募基金管理人名称', '法定代表人', '机构类型', '注册地',
                                 '登记编号', '成立时间', '登记时间', '全职员工人数', '取得基金从业人数', '律师事务所名称', '律师姓名'])
writer = pd.ExcelWriter('私募基金清单.xlsx')
df.to_excel(writer, sheet_name='私募基金清单')
writer.save()
