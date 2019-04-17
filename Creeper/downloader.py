''' 获取网页内容 '''
import urllib
import requests

cookies = {}


def get_html(url, request_data={}, method='post', header={}, cookie={}):
    ''' 获取页面 '''
    if method == 'post':
        r = requests.post(url, data=request_data,
                          headers=header, cookies=cookie)
    else:
        r = requests.get(url, params=request_data,
                         headers=header, cookies=cookie)
    
    if r.status_code == requests.codes.ok:
        # r.raw对象 r.content二进制 r.json()解析JSON
        r.encoding = 'utf-8'
        return r.text
    else:
        print(r.text)
        return ''
