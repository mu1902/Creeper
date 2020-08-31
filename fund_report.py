''' 爬取证监会基金公告数据 '''
import datetime
import json
import random
import time
import sys

import Creeper as cp

urls = {"csrc": "http://eid.csrc.gov.cn/fund/disclose/upload_info_list_page.do"}

companies = ["东证", "汇添富", "易方达", "富国", "兴全", "交银", "广发"]
codes = ["110011", "000083", "005379", "260108",
         "162605", "163406", "163417", "000940", 
         "001268", "519772", "519736", "008418", "399011", "007119"]

today = datetime.date.today().strftime('%Y-%m-%d')
yesterday = (datetime.date.today() -
             datetime.timedelta(days=1)).strftime('%Y-%m-%d')
param = [{"name": "sEcho", "value": 1},
         {"name": "iColumns", "value": 6},
         {"name": "sColumns", "value": ",,,,,"},
         {"name": "iDisplayStart", "value": 0},
         {"name": "iDisplayLength", "value": 20},
         {"name": "mDataProp_0", "value": "fundCode"},
         {"name": "mDataProp_1", "value": "fundId"},
         {"name": "mDataProp_2", "value": "organName"},
         {"name": "mDataProp_3", "value": "reportName"},
         {"name": "mDataProp_4", "value": "reportSendDate"},
         {"name": "mDataProp_5", "value": "reportDesp"},
         {"name": "fundCompanyShortName", "value": ""},
         {"name": "fundCompanyCode", "value": ""},
         {"name": "fundCode", "value": ""},
         {"name": "fundShortName", "value": ""},
         {"name": "fundType", "value": ""},
         {"name": "reportTypeCode", "value": "FB"},
         {"name": "reportYear", "value": ""},
         {"name": "startUploadDate", "value": yesterday},
         {"name": "endUploadDate", "value": today}]

message = ""
num = 0
for c in codes:
    param[13]["value"] = c
    timestamp = int(time.time()*1000)
    reports = cp.downloader.get_html(urls['csrc'], request_data={
        "aoData": json.dumps(param), "_": str(timestamp)}, method='get')
    reports = json.loads(reports)
    num += reports["iTotalRecords"]
    for r in reports["aaData"]:
        message += r["reportName"]+"\n"
        message += "http://eid.csrc.gov.cn/fund/disclose/instance_show_pdf_id.do?instanceid=" + \
            str(r["uploadInfoId"])+"\n"
    time.sleep(0.1)

message += "--------以下是公司--------\n"

for c in companies:
    param[13]["value"] = ""
    param[11]["value"] = c
    timestamp = int(time.time()*1000)
    reports = cp.downloader.get_html(urls['csrc'], request_data={
        "aoData": json.dumps(param), "_": str(timestamp)}, method='get')
    reports = json.loads(reports)
    num += reports["iTotalRecords"]
    for r in reports["aaData"]:
        message += r["reportName"]+"\n"
        message += "http://eid.csrc.gov.cn/fund/disclose/instance_show_pdf_id.do?instanceid=" + \
            str(r["uploadInfoId"])+"\n"
    time.sleep(0.1)

print(num)
# print(message)
if num == 0:
    cp.tool.send_email([], '关注基金公告', '无')
else:
    cp.tool.send_email(["zhengy@xunlc.cn"], '关注基金公告', message)
