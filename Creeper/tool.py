''' 爬虫相关功能 '''
import math
import sys

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
        'db': db
    }
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = ''

    for i in res_list:
        print(i)
        tmplist = []
        for k, v in i.items():
            tmp = "%s='%s'" % (str(k), safe(str(v)))
            tmplist.append(' ' + tmp + ' ')
        sql = 'INSERT INTO ' + table + ' SET ' + ' and '.join(tmplist)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    db.close()


def progressbar(cur, total):
    ''' 进度条显示 '''
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)),
                                     percent))
    sys.stdout.flush()
