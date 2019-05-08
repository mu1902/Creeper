import datetime
import sys

import numpy as np
import pandas as pd
from WindPy import w

TEST_FUNDS = "000001.OF,000003.OF,000004.OF,000005.OF,000006.OF,000008.OF,000009.OF,000010.OF"

if __name__ == '__main__':
    # fund_list = []
    # try:
    #     file_object = open('./funds.txt', mode='r', encoding='UTF-8')
    #     fund_list = file_object.readlines()
    #     file_object.close()
    # except FileNotFoundError as e:
    #     print(e)

    # fund_list = [f.replace('\n', '') for f in fund_list]
    # # print(','.join(fund_list))

    w.start()
    funds = w.wss("000001.OF,000003.OF,000004.OF,000005.OF,000006.OF,000008.OF,000009.OF,000010.OF",
                  "fund_fullname,fund_firstinvesttype,fund_investtype,fund_themetype,fund_type,fund_trackindexcode,fund_etfwindcode,prt_netasset", "unit=1;rptDate=20181231")

    if funds.ErrorCode == 0:
        funds_df = pd.DataFrame(funds.Data, index=funds.Fields,
                                columns=funds.Codes).T
    else:
        print(funds.Data)
        sys.exit(0)
    w.stop()

    funds_df = funds_df.drop('FUND_THEMETYPE', axis=1).join(funds_df['FUND_THEMETYPE'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('FUND_THEMETYPE'))
    print(funds_df)
    
    # writer = pd.ExcelWriter('funds.xlsx')
    # funds_df.to_excel(writer, sheet_name='funds')
    # funds_stocks_df.to_excel(writer, sheet_name='now')
    # funds_stocks_df2.to_excel(writer, sheet_name='pre')
    # writer.save()
