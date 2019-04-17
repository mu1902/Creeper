''' 爬虫相关功能 '''
import datetime
import math
import smtplib
import sys
from email.mime.text import MIMEText

import pymysql
import xlwt

_dir = "D:/workspace/Creeper"


def to_excel(res_list, filename):
    ''' 生成EXCEL文件 '''
    print("\n创建EXCEL文件......")
    try:
        excel = xlwt.Workbook()
        sheet = excel.add_sheet("my_sheet")
        for row in range(0, len(res_list)):
            for col in range(0, len(res_list[row])):
                sheet.write(row, col, res_list[row][col])
        excel.save(filename + ".xls")
    except:
        print("创建失败:" + sys.exc_info()[0])
    print("创建完成")


def to_mysql(res_list, db, table):
    ''' 保存至MySQL数据库 '''
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'j9mkmuko',
        'db': db,
        'charset': 'utf8'
    }
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = ''
    res = 0

    for i in res_list:
        keys = []
        values = []
        for k, v in i.items():
            keys.append(k)
            values.append("'" + str(v) + "'")
        sql = 'INSERT INTO ' + table + \
            '(' + ','.join(keys) + ') VALUES (' + ','.join(values) + ')'
        # print(sql)
        try:
            res += cursor.execute(sql)
            db.commit()
        except:
            print("数据库出错:" + sql)
            db.rollback()

    db.close()
    return res

def send_email(to_list, subject, massage):
    mail_host = "smtp.exmail.qq.com"
    mail_user = "fund@fundbj.com"
    mail_pwd = "fed68390036"
    msg = MIMEText(massage, _subtype='plain', _charset='gb2312')
    msg['Subject'] = subject
    msg['From'] = mail_user
    msg['To'] = ";".join(to_list)
    msg['Bcc'] = 'chuh@fundbj.com'
    server = smtplib.SMTP()
    server.connect(mail_host)
    server.login(mail_user, mail_pwd)
    server.sendmail(mail_user, to_list, msg.as_string())
    server.close()

def progressbar(cur, total):
    ''' 进度条显示 '''
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)),
                                     percent))
    sys.stdout.flush()


def isHoliday(day):
    days = []
    try:
        file_object = open(_dir + '/restday.txt', mode='r', encoding='UTF-8')
        days = file_object.readlines()
        file_object.close()
    except FileNotFoundError as e:
        print(e)

    day = datetime.datetime.strptime(str(day),'%Y-%m-%d')
    days = [datetime.datetime.strptime(d[:-1], "%Y.%m.%d") for d in days]
    if day.weekday() == 5 or day.weekday() == 6 or day in days:
        return True
    else:
        return False


def preDay(day):
    d = day - datetime.timedelta(days=1)
    while isHoliday(d):
        d = d - datetime.timedelta(days=1)
    return d
