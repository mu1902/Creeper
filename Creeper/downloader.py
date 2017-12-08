''' 获取网页内容 '''
import urllib

cookies = {}

def get_html(url, request_data=None, method='post', header=None, cookie_name=None):
    ''' 获取页面 '''
    if cookie_name:
        cookie = cookies.setdefault(cookie_name, http.cookiejar.CookieJar())  # 声明一个CookieJar对象实例来保存cookie
        handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用urllib库的HTTPCookieProcessor对象来创建cookie处理器
        opener = urllib.request.build_opener(handler)  # 通过handler来构建opener
    try:
        if request_data:
            if method == 'post':
                data = urllib.parse.urlencode(request_data).encode('utf_8')
                req = urllib.request.Request(url, data)
            else:
                data = urllib.parse.urlencode(request_data)
                req = urllib.request.Request(url + data)
        else:
            req = urllib.request.Request(url)

        if header:
            for key in header:
                req.add_header(key, header[key])
        if cookie_name:
            con = opener.open(req).read()
        else:
            con = urllib.request.urlopen(req).read()
        return con
    except urllib.error.HTTPError as e:
        # print(e)
        return ''
    except urllib.error.URLError as e:
        # print(e)
        return ''
