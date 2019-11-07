import datetime
import sys

import numpy as np
import pandas as pd
from WindPy import w

MIN_RETURN = 5
MIN_YEARS = 5
REPORT_DATE = '20190930'
REPORT_DATE_PRE = '20190630'

if __name__ == '__main__':
    fund_list = []
    fund_list_all = []
    try:
        file_object = open('./funds.txt', mode='r', encoding='UTF-8')
        file_object2 = open('./funds_all.txt', mode='r', encoding='UTF-8')
        fund_list = file_object.readlines()
        fund_list_all = file_object2.readlines()
        file_object.close()
        file_object2.close()
    except FileNotFoundError as e:
        print(e)

    fund_list = [f.replace('\n', '') for f in fund_list]
    fund_list_all = [f.replace('\n', '') for f in fund_list_all]

    w.start()

    funds = w.wss(','.join(fund_list),
                  "fund_fullname,fund_setupdate,fund_fundmanager,fund_manager_fundno,fund_manager_totalnetasset,fund_manager_startdate,fund_manager_onthepostdays,fund_manager_geometricannualizedyield,fund_manager_arithmeticannualizedyield,fund_manager_managerworkingyears", "order=1;unit=1;returnType=1")
    if funds.ErrorCode != 0:
        print(funds.Data)
        sys.exit(0)
    funds_df = pd.DataFrame(funds.Data, index=funds.Fields,
                            columns=funds.Codes).T
    funds_df['order'] = 1

    # funds = w.wss(','.join(fund_list),
    #               "fund_fullname,fund_setupdate,fund_fundmanager,fund_manager_fundno,fund_manager_totalnetasset,fund_manager_startdate,fund_manager_onthepostdays,fund_manager_geometricannualizedyield,fund_manager_arithmeticannualizedyield,fund_manager_managerworkingyears", "order=2;unit=1;returnType=1")
    # if funds.ErrorCode != 0:
    #     print(funds.Data)
    #     sys.exit(0)
    # funds_df2 = pd.DataFrame(funds.Data, index=funds.Fields,
    #                         columns=funds.Codes).T
    # funds_df2['order'] = 2

    # funds = w.wss(','.join(fund_list),
    #               "fund_fullname,fund_setupdate,fund_fundmanager,fund_manager_fundno,fund_manager_totalnetasset,fund_manager_startdate,fund_manager_onthepostdays,fund_manager_geometricannualizedyield,fund_manager_arithmeticannualizedyield,fund_manager_managerworkingyears", "order=3;unit=1;returnType=1")
    # if funds.ErrorCode != 0:
    #     print(funds.Data)
    #     sys.exit(0)
    # funds_df3 = pd.DataFrame(funds.Data, index=funds.Fields,
    #                         columns=funds.Codes).T
    # funds_df3['order'] = 3

    # funds_df.append(funds_df2)
    # funds_df.append(funds_df3)
    funds_df = funds_df[(funds_df['FUND_MANAGER_MANAGERWORKINGYEARS'] >
                         MIN_YEARS) & (funds_df['FUND_MANAGER_GEOMETRICANNUALIZEDYIELD'] > MIN_RETURN)]
    codes = funds_df.index.tolist()

    for i in range(1, 11):
        funds_stocks = w.wss(",".join(
            codes), "prt_topstockwindcode,prt_topstockname,prt_topproportiontofloating,prt_heavilyheldstocktonav,prt_fundnoofstocks", "rptDate="+REPORT_DATE+";order="+str(i))
        if funds_stocks.ErrorCode != 0:
            print(funds_stocks.Data)
            sys.exit(0)
        if i == 1:
            funds_stocks_df = pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                           columns=funds_stocks.Codes).T
        else:
            funds_stocks_df = funds_stocks_df.append(pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                                                  columns=funds_stocks.Codes).T)
    funds_stocks_df = funds_stocks_df.sort_index()

    for i in range(1, 11):
        funds_stocks = w.wss(",".join(
            codes), "prt_topstockwindcode,prt_topstockname,prt_topproportiontofloating,prt_heavilyheldstocktonav,prt_fundnoofstocks", "rptDate="+REPORT_DATE_PRE+";order="+str(i))
        if funds_stocks.ErrorCode != 0:
            print(funds_stocks.Data)
            sys.exit(0)
        if i == 1:
            funds_stocks_df2 = pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                            columns=funds_stocks.Codes).T
        else:
            funds_stocks_df2 = funds_stocks_df2.append(pd.DataFrame(funds_stocks.Data, index=funds_stocks.Fields,
                                                                    columns=funds_stocks.Codes).T)
    funds_stocks_df2 = funds_stocks_df2.sort_index()

    funds_type = w.wss(
        ','.join(fund_list_all[:5000]), "fund_fullname,fund_firstinvesttype,fund_investtype,fund_themetype,fund_type,fund_trackindexcode,fund_etfwindcode,prt_netasset", "unit=1;rptDate="+REPORT_DATE)
    if funds_type.ErrorCode != 0:
        print(funds_type.Data)
        sys.exit(0)
    funds_type2 = w.wss(
        ','.join(fund_list_all[5001:]), "fund_fullname,fund_firstinvesttype,fund_investtype,fund_themetype,fund_type,fund_trackindexcode,fund_etfwindcode,prt_netasset", "unit=1;rptDate="+REPORT_DATE)
    if funds_type2.ErrorCode != 0:
        print(funds_type2.Data)
        sys.exit(0)

    funds_type_df = pd.DataFrame(funds_type.Data, index=funds_type.Fields,
                                 columns=funds_type.Codes).T
    funds_type_df = funds_type_df.append(pd.DataFrame(funds_type2.Data, index=funds_type2.Fields,
                                                      columns=funds_type2.Codes).T)
    funds_type_df = funds_type_df.drop('FUND_THEMETYPE', axis=1).join(funds_type_df['FUND_THEMETYPE'].str.split(
        ',', expand=True).stack().reset_index(level=1, drop=True).rename('FUND_THEMETYPE'))

    w.stop()

    writer = pd.ExcelWriter('funds.xlsx')
    funds_df.to_excel(writer, sheet_name='funds')
    funds_stocks_df.to_excel(writer, sheet_name='now')
    funds_stocks_df2.to_excel(writer, sheet_name='pre')
    funds_type_df.to_excel(writer, sheet_name='type')
    writer.save()
