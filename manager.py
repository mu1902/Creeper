import datetime
import sys

import numpy as np
import pandas as pd
from WindPy import w

MIN_RETURN = 5
MIN_YEARS = 5
REPORT_DATE = '20181231'
REPORT_DATE_PRE = '20180930'

if __name__ == '__main__':
    fund_list = []
    try:
        file_object = open('./funds.txt', mode='r', encoding='UTF-8')
        fund_list = file_object.readlines()
        file_object.close()
    except FileNotFoundError as e:
        print(e)

    fund_list = [f.replace('\n', '') for f in fund_list]
    # print(','.join(fund_list))

    w.start()
    funds = w.wss(','.join(fund_list),
                  "fund_fundmanager,fund_fullname,fund_manager_managerworkingyears,fund_manager_geometricannualizedyield", "order=1;returnType=1")
    if funds.ErrorCode == 0:
        funds_df = pd.DataFrame(funds.Data, index=funds.Fields,
                                columns=funds.Codes)
        funds_df = funds_df.T
    else:
        print(funds.Data)
        sys.exit(0)

    funds_df = funds_df[(funds_df['FUND_MANAGER_MANAGERWORKINGYEARS'] >
                         MIN_YEARS) & (funds_df['FUND_MANAGER_GEOMETRICANNUALIZEDYIELD'] > MIN_RETURN)]
    # print(funds_df)

    codes = funds_df.index.tolist()
    # print(codes)

    for i in range(1, 11):
        funds_stocks = w.wss(",".join(
            codes), "prt_topstockwindcode,prt_topstockname,prt_topproportiontofloating,prt_heavilyheldstocktonav,prt_fundnoofstocks", "rptDate="+REPORT_DATE+";order="+str(i))
        if funds_stocks.ErrorCode == 0:
            if i == 1:
                funds_stocks_df = pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                               columns=funds_stocks.Codes).T
            else:
                funds_stocks_df = funds_stocks_df.append(pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                                                      columns=funds_stocks.Codes).T)
        else:
            print(funds_stocks.Data)
            sys.exit(0)

    funds_stocks_df = funds_stocks_df.sort_index()
    # print(funds_stocks_df)

    for i in range(1, 11):
        funds_stocks = w.wss(",".join(
            codes), "prt_topstockwindcode,prt_topstockname,prt_topproportiontofloating,prt_heavilyheldstocktonav,prt_fundnoofstocks", "rptDate="+REPORT_DATE_PRE+";order="+str(i))
        if funds_stocks.ErrorCode == 0:
            if i == 1:
                funds_stocks_df2 = pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                                columns=funds_stocks.Codes).T
            else:
                funds_stocks_df2 = funds_stocks_df2.append(pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                                                        columns=funds_stocks.Codes).T)
        else:
            print(funds_stocks.Data)
            sys.exit(0)

    funds_stocks_df2 = funds_stocks_df2.sort_index()

    w.stop()

    writer = pd.ExcelWriter('funds.xlsx')
    funds_df.to_excel(writer, sheet_name='funds')
    funds_stocks_df.to_excel(writer, sheet_name='now')
    funds_stocks_df2.to_excel(writer, sheet_name='pre')
    writer.save()
