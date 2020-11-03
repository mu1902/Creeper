''' 获取网页内容 '''
import urllib3
import requests
import ssl

urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
cookies = {}


def get_html(url, request_data={}, method='post', header={}, cookie={}, code='', ret_cookies=False):
    ''' 获取页面 '''
    try:
        if method == 'post':
            r = requests.post(url, data=request_data,
                              headers=header, cookies=cookie, timeout=5000, verify=False, allow_redirects=False)
        else:
            r = requests.get(url, params=request_data,
                             headers=header, cookies=cookie, timeout=5000, verify=False, allow_redirects=False)

        if ret_cookies:
            # print(r.status_code)
            # print(r.headers)
            return r.cookies.get_dict()

        if r.status_code == requests.codes.ok:
            # r.raw对象 r.content二进制 r.json()解析JSON
            r.encoding = code if code != '' else 'utf-8'
            return r.text
        else:
            print(r.text)
            return ''
    except Exception as e:
        print(e)
        return ''


def get_file(url, file_url):
    try:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            with open(file_url, "wb") as f:
                f.write(r.content)
                return f
        else:
            print(r.text)
            return ''
    except Exception as e:
        print(e)
        return ''
