import tushare as ts
import sqlalchemy as sa
import multiprocessing as mp
import pandas as pd
import datetime as dt
import sys


def get_daily_quote(cal):
    '''获得每日报价信息，按交易日历，获取所有股票的报价信息'''
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
    for c in cal:
        df = pro.daily(trade_date=c)
        df.to_sql(name='daily_quote', con=eng, if_exists='append', index=False)
        #print('Get %s quote.' % c)


def get_adj_factor(cal):
    '''获得复权因子，按交易日历，获取所有股票的复权因子'''
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
    for c in cal:
        df = pro.adj_factor(ts_code='', trade_date=c)
        df.to_sql(name='adj_factor', con=eng, if_exists='append', index=False)
        #print('Get %s factor.' % c)


def get_daily_indicator(cal):
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
    for c in cal:
        df = pro.daily_basic(ts_code='', trade_date=c)
        df.to_sql(name='daily_indicator', con=eng, if_exists='append', index=False)
        #print('Get %s indicator.' % c)


def get_dividend(tscode):
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
    for tsc in tscode:
        df = pro.dividend(ts_code=tsc)
        df.to_sql(name='dividend', con=eng, if_exists='append', index=False)
        #print('Get %s dividend.' % tsc)


if __name__ == '__main__':
    g_bng = dt.datetime.now()
    g_eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
    #
    pN = mp.cpu_count()*2
    pl = mp.Pool(processes=pN)
    #
    if sys.argv[1] == 'daily':
        cal = pd.read_sql_table(table_name='trade_cal', con=g_eng, columns=('cal_date', 'is_open'))
        cal = cal[cal.is_open == 1]['cal_date']
        cal = cal.tolist()
        step = int(len(cal) / pN)
        for i in range(pN-1):
            pl.apply_async(func=get_daily_quote, args=(cal[(i*step):((i+1)*step)],))
        #
        pl.apply_async(func=get_daily_quote, args=(cal[(pN-1)*step:],))
    elif sys.argv[1] == 'factor':
        cal = pd.read_sql_table(table_name='trade_cal', con=g_eng, columns=('cal_date', 'is_open'))
        cal = cal[cal.is_open == 1]['cal_date']
        cal = cal.tolist()
        step = int(len(cal) / pN)
        for i in range(pN-1):
            pl.apply_async(func=get_adj_factor, args=(cal[(i*step):((i+1)*step)],))
        #
        pl.apply_async(func=get_adj_factor, args=(cal[(pN-1)*step:],))
    elif sys.argv[1] == 'indicator':
        cal = pd.read_sql_table(table_name='trade_cal', con=g_eng, columns=('cal_date', 'is_open'))
        cal = cal[cal.is_open == 1]['cal_date']
        cal = cal.tolist()
        step = int(len(cal) / pN)
        for i in range(pN-1):
            pl.apply_async(func=get_daily_indicator, args=(cal[(i*step):((i+1)*step)],))
        #
        pl.apply_async(func=get_daily_indicator, args=(cal[(pN-1)*step:],))
    elif sys.argv[1] == 'dividend':
        tsc = pd.read_sql_table(table_name='stock_basic', con=g_eng, columns=('ts_code', 'list_status'))
        tsc = tsc[tsc.list_status == 'L']['ts_code']
        tsc = tsc.tolist()
        step = int(len(tsc) / pN)
        for i in range(pN-1):
            pl.apply_async(func=get_dividend, args=(tsc[(i*step):((i+1)*step)],))
        #
        pl.apply_async(func=get_daily_indicator, args=(tsc[(pN-1)*step:],))
    else:
        print('command:')
        print("python %s daily/factor/indicator/dividend" % __file__)
        sys.exit(-1)
    #
    pl.close()
    pl.join()

    print('%s run %0.2f seconds.' % (__file__,(dt.datetime.now()-g_bng).total_seconds()))
