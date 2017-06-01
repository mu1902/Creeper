''' 调度器 '''
from queue import Queue
from threading import Thread

import downloader


class Scheduler(object):

    def __init__(self, url_manager):
        self.__tasks = url_manager
        self._size = 10
        self.res_list = []

    def start(self, parse_content_fn, parse_url_fn=None):
        self.__task_q = Queue(self._size)
        print("Start")
        while not self.__tasks.isdone():
            url = self.__tasks.get_one()
            con = downloader.get_html(url)
            self.res_list.extend(parse_content_fn(con))
            if parse_url_fn:
                self.__tasks.add_url(None, parse_url_fn(con))
            self.__tasks.fin_url(url)
        print("Done")

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if type(value) == 'int':
            self._size = value


class MyThread(threading.Thread):

    def __init__(self, target, args):
        super(MyThread, self).__init__()
        self.target = target
        self.args = args

    def run(self):
        apply(self.target, self.args)
