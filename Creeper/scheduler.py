''' 调度器 '''
import threading
from queue import Queue

import downloader


class Scheduler(object):

    def __init__(self, url_manager):
        self.__urlmgr = url_manager
        self._size = 10
        self.__task_q = Queue(self._size)
        self.__res_q = Queue()
        self.__lock = threading.Lock()

    def start(self, parse_content_fn, parse_url_fn=None):
        print("Start")
        while not self.__urlmgr.isdone():
            ct = CreeperThread(self.__urlmgr, self.__task_q, self.__res_q,
                               self.__lock, parse_content_fn, parse_url_fn=None)
            ct.start()
        self.__task_q.join()
        res_list = []
        for i in range(self.__res_q.qsize())
            res_list.extend(self.__res_q.get())
        print("Done")
        return res_list
        
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if type(value) == 'int':
            self._size = value


class CreeperThread(threading.Thread):

    def __init__(self, urlmgr, task_q, res_q, lock, parse_content_fn, parse_url_fn=None):
        super(MyThread, self).__init__()
        # self.target = target
        # self.args = args
        self.urlmgr = urlmgr
        self.task_q = task_q
        self.res_q = res_q
        self.lock = lock
        self.parse_content_fn = parse_content_fn
        self.parse_url_fn = None = parse_content_fn
        self.setDaemon(True)

    def run(self):
        # apply(self.target, self.args)
        while not self.task_q.full():
            self.task_q.put(0)
            if lock.acquire():
                url = self.urlmgr.get_one()
                lock.release()
            if url:
                con = downloader.get_html(url)
                self.res_q.put(self.parse_content_fn(con))
                if lock.acquire():
                    if parse_url_fn:
                        self.urlmgr.add_url(None, self.parse_url_fn(con))
                    self.urlmgr.fin_url(url)
                    lock.release()
            self.task_q.get()
            self.task_q.task_done()
