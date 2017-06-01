''' url管理器 '''


class UrlManager(object):

    def __init__(self, url_base):
        self.__base = url_base
        self.url_future = set()
        self.url_past = set()

    def add_url(self, item=None, item_list=[]):
        if item:
            self.url_future.add(i)
        self.url_future.extend(item_list)

    def fin_url(self, item):
        self.url_future.discard(item)
        self.url_past.add(item)

    def get_one(self):
        if len(self.url_future) > 0:
            return self.__base + self.url_future.pop()
        else:
            return None

    def is_done(self):
        if len(self.url_future) == 0:
            return True
        else:
            return False
