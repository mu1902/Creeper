import datetime

import Creeper as cp

if __name__ == '__main__':
    dn = datetime.date(2018,1,1)
    print(cp.tool.isHoliday(dn))