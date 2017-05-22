''' 爬虫核心类 '''
import urllib as ul

def getHtml(url):
    ''' 获取页面 '''
    content = ul.urlopen(url).read()

