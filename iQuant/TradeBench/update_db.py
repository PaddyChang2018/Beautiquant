import tushare as ts
import sqlalchemy as sa
import multiprocessing as mp
import datetime as dt
import sys
import pandas as pd
import iQuant.TradeBench.initdb_multiproc as qt


if __name__ == '__main__':
    # record start time
    g_bng = dt.datetime.now()
    if len(sys.argv) == 2:
        g_end_date = dt.datetime.now().strftime('%Y%m%d')
    elif len(sys.argv) == 3:
        g_end_date = sys.argv[2]
    else:
        print('python %s %s [%s]' % (__file__, 'start_date', 'end_date'))
        print('%s run %0.2f seconds.' % (__file__, (dt.datetime.now() - g_bng).total_seconds()))
        sys.exit(-1)

    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
    cal = pro.trade_cal(exchange='', start_date=sys.argv[1], end_date=g_end_date)
    cal.to_sql(name='trade_cal', con=eng, if_exists='append', index=False)
    cal = cal[cal.is_open == 1]['cal_date']
    cal = cal.tolist()
    #
    pool = mp.Pool(processes=mp.cpu_count()*2)
    pool.apply_async(func=qt.get_adj_factor, args=(cal,))
    pool.apply_async(func=qt.get_daily_indicator, args=(cal,))
    pool.apply_async(func=qt.get_daily_quote, args=(cal,))
    #
    tc = pd.read_sql_table(table_name='stock_basic', con=eng, columns=('ts_code', 'list_status'))
    tc = tc[tc.list_status == 'L']['ts_code']
    tc = tc.tolist()
    pool.apply_async(func=qt.get_income, args=(tc, cal[0], cal[-1]))
    pool.apply_async(func=qt.get_balance, args=(tc, cal[0], cal[-1]))
    #
    pool.close()
    pool.join()
    print('%s run %0.2f seconds.' % (__file__, (dt.datetime.now() - g_bng).total_seconds()))
