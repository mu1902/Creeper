''' 获取网页内容 '''
import urllib


def get_html(url, post_data=None):
    ''' 获取页面 '''
    req = urllib.request.Request(url)
    if post_data:
        data = urllib.parse.urlencode(post_data).encode('utf-8')
        con = urllib.request.urlopen(req, data).read()
    else:
        con = urllib.request.urlopen(req).read()
    return con
