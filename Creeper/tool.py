''' 爬虫相关功能 '''
import math
import sys
import datetime

import xlwt
import pymysql


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
    print(res)
    return res


def progressbar(cur, total):
    ''' 进度条显示 '''
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)),
                                     percent))
    sys.stdout.flush()


def isTradingDay(day):
    days = []
    try:
        file_object = open('restday.txt', mode='r', encoding='UTF-8')
        days = file_object.readlines()
        file_object.close()
    except FileNotFoundError as e:
        print(e)
        
    days = [datetime.datetime.strptime(d[:-1], "%Y.%m.%d") for d in days]
    if day.weekday() == 5 or day.weekday() == 6 or day in days:
        return True
    else:
        return False
