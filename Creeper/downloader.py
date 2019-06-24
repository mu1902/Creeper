''' 获取网页内容 '''
import urllib
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context #requests verify=False
cookies = {}


def get_html(url, request_data={}, method='post', header={}, cookie={}):
    ''' 获取页面 '''
    try:
        if method == 'post':
            r = requests.post(url, data=request_data,
                            headers=header, cookies=cookie, timeout=5000)
        else:
            r = requests.get(url, params=request_data,
                            headers=header, cookies=cookie, timeout=5000)
        
        if r.status_code == requests.codes.ok:
            # r.raw对象 r.content二进制 r.json()解析JSON
            r.encoding = 'utf-8'
            return r.text
        else:
            print(r.text)
            return ''
    except Exception as e:
        print(e)
        return ''
