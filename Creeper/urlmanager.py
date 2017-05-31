''' url管理器 '''


class UrlManager(object):

    def __init__(self):
        self.url_future = set()
        self.url_past = set()

    def add_url(self, item=None, list=[]):
        if item:
            self.url_future.add(i)
        for i in list:
            self.url_future.add(i)

    def fin_url(self, item):
        self.url_future.discard(item)
        self.url_past.add(item)

    def get_one(self)
        return self.url_future.pop()
