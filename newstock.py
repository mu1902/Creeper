''' 新股开板提醒 '''
import datetime
import urllib


if __name__ == '__main__':
    req = urllib.request.Request('http://hq.sinajs.cn/list=sh603855')
    res = urllib.request.urlopen(req).read()
    print("名称：" + res[0])
    print("昨收：" + res[2])
    print("当前：" + res[3])
    print("成交量：" + res[8]/100)
    print("成交额：" + res[9]/10000)
    print("买一量" + res[10]/100)
    print("买二量" + res[12]/100)