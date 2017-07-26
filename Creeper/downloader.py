''' 获取网页内容 '''
import urllib


def get_html(url, request_data=None, method='post', header=None):
    ''' 获取页面 '''
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
        con = urllib.request.urlopen(req).read()
        return con
    except urllib.error.HTTPError as e:
        print(e)
        return ''
    except urllib.error.URLError as e:
        print(e)
        return ''
