import datetime
import sys

import numpy as np
import pandas as pd
from WindPy import w

index = ['000300.SH',
'716567.CSI',
'SPCLLHCP.SPI',
'h30089.CSI',
'931079.CSI',
'930606.CSI',
'399998.SZ']


if __name__ == '__main__':
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    return_df = pd.DataFrame()

    w.start()
    for idx in index:
        index_list = w.wset("indexconstituent","date="+date_str+"windcode="+idx)

        if index_list.ErrorCode == 0:
            tmp_df = pd.DataFrame(index_list.Data, index=index_list.Fields,
                                    columns=index_list.Codes).T
            tmp_df['index'] = idx
            return_df = return_df.append(tmp_df)
        else:
            print(index_list.Data)
            sys.exit(0)
    w.stop()

    print(return_df)
    
    writer = pd.ExcelWriter('indexlist.xlsx')
    return_df.to_excel(writer, sheet_name='indexlist')
    writer.save()
