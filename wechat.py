import datetime as dt
import os
import re
import time

from pysqlcipher3 import dbapi2 as sqlite
import Creeper as cp

os.system('nox_adb pull /data/data/com.tencent.mm/MicroMsg/87c8969adadf852b441173a366e2be9e/EnMicroMsg.db D:\Files\Wechat')

PWD = '9c22ae0'
DB_PATH = 'D:\Files\Wechat\EnMicroMsg.db'

t = int(time.mktime(dt.date.today().timetuple()))*1000
sql = '''
select m.createTime, m.content, c.nickname
  from message as m, rcontact as c
 where m.type=285212721
   and c.nickname="上海发布"
   and m.talkerId=c.rowid
   and m.createTime>{0};
'''.format(t)

conn = sqlite.connect(DB_PATH)
curs = conn.cursor()
curs.execute("PRAGMA key='" + PWD + "';")
curs.execute("PRAGMA kdf_iter = '4000';")
curs.execute("PRAGMA cipher_use_hmac = OFF;")
curs.execute(sql)

message = ''
for row in curs:
    message += row[2] + '\n'
    rawtxt = re.sub('([\x00-\x10]|\xd0)+?', '', row[1])
    count_str_arr = re.findall('\$count(\d+?)', rawtxt, re.S)
    count = int(count_str_arr[0]) if len(count_str_arr) > 0 else 0
    for i in range(count):
        c = str(i) if i > 0 else ''
        title = re.findall('item'+c+'\.title(.+?)\.msg', rawtxt, re.S)
        url = re.findall('item'+c+'\.url(.+?)&chksm=', rawtxt, re.S)
        message += title[0] + '\n' + url[0] + '\n'
    message += '\n'

conn.close()


cp.tool.send_email([], '今日公众号文章', message)
