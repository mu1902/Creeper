''' 爬虫相关功能 '''
import math
import sys

import xlwt


def to_excel(res_list, filename):
    ''' 生成EXCEL文件 '''
    print("\n创建EXCEL文件......")
    excel = xlwt.Workbook()
    sheet = excel.add_sheet("my_sheet")
    for row in range(0, len(res_list)):
        for col in range(0, len(res_list[row])):
            sheet.write(row, col, res_list[row][col])
    excel.save(filename + ".xls")
    print("完成")


def progressbar(cur, total):
    ''' 进度条显示 '''
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)),
                                     percent))
    sys.stdout.flush()
