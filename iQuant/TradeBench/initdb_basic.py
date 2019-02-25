import tushare as ts
import sqlalchemy as sa
import multiprocessing as mp
import datetime as dt
import sys


def get_stock_basic(list_status_flag):
    # create tushare pro object
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    #bgn = dt.datetime.now()
    #print("Get stock_basic %s start at %s" % (list_status_flag, bgn))
    # get stock basic data from tushare
    df = pro.stock_basic(list_status=list_status_flag,
                         fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,'
                                'list_date,delist_date,is_hs')
    #end = dt.datetime.now()
    #print("Get stock_basic %s end at %s spend on %0.2f seconds." % (list_status_flag, end, (end - bgn).total_seconds()))
    return {'tbl':'stock_basic','flag':list_status_flag,'data':df}


def get_hs_const(type):
    # create tushare pro object
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    #bgn = dt.datetime.now()
    #print("Get hs_const %s start at %s" % (type, bgn))
    df = pro.hs_const(hs_type=type)
    #end = dt.datetime.now()
    #print("Get hs_const %s end at %s spend on %0.2f seconds." % (type, end, (end - bgn).total_seconds()))
    return {'tbl':'hs_const', 'flag':type, 'data':df}


def get_stock_company(exchange):
    # create tushare pro object
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    #bgn = dt.datetime.now()
    #print("Get stock_company %s start at %s" % (exchange, bgn))
    df = pro.stock_company(exchange='SZSE',
                             fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,'
                                    'introduction,website,email,office,employees,main_business,business_scope')
    #end = dt.datetime.now()
    #print("Get stock_company %s end at %s spend on %0.2f seconds." % (exchange, end, (end - bgn).total_seconds()))
    return {'tbl':'stock_company', 'flag':exchange, 'data':df}


def get_trade_cal(startdate, enddate):
    # create tushare pro object
    pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
    #bgn = dt.datetime.now()
    #print("Get trade_cal %s-%s start at %s" % (startdate, enddate, bgn))
    df = pro.trade_cal(exchange='', start_date=startdate, end_date=enddate)
    #end = dt.datetime.now()
    #print("Get trade_cal %s-%s end at %s cost %0.2f seconds." % (startdate, enddate, end, (end - bgn).total_seconds()))
    return {'tbl':'trade_cal', 'flag':'', 'data':df}

def to_database(ddct):
    if len(ddct['data']) > 0:
        # create database engine
        db_eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
        # write stock basic data into databasae
        #bgn = dt.datetime.now()
        #print("Write table %s %s start at %s" % (ddct['tbl'],ddct['flag'],bgn))
        ddct['data'].to_sql(name=ddct['tbl'], con=db_eng, if_exists='append', index=False)
        #end = dt.datetime.now()
        #print("Write table %s %s end at %s spend on %0.2f seconds." % (ddct['tbl'], ddct['flag'], end, (end - bgn).total_seconds()))


if __name__== '__main__':
    # record start time
    bng = dt.datetime.now()
    # create process pool
    pool = mp.Pool(processes = mp.cpu_count()*2)
    pool.apply_async(func=get_stock_basic, args=('L',), callback=to_database)
    pool.apply_async(func=get_stock_basic, args=('D',), callback=to_database)
    pool.apply_async(func=get_stock_basic, args=('P',), callback=to_database)
    pool.apply_async(func=get_hs_const, args=('SH',), callback=to_database)
    pool.apply_async(func=get_hs_const, args=('SZ',), callback=to_database)
    pool.apply_async(func=get_stock_company, args=('SSE',), callback=to_database)
    pool.apply_async(func=get_stock_company, args=('SZSE',), callback=to_database)
    if len(sys.argv) == 3:
        pool.apply_async(func=get_trade_cal, args=(sys.argv[1], sys.argv[2]), callback=to_database)
    else:
        pool.apply_async(func=get_trade_cal, args=('20160101', '20181220'), callback=to_database)
    #
    pool.close()
    pool.join()
    # print spend time
    print("%s run %0.2f seconds." %(__file__, (dt.datetime.now() - bng).total_seconds()))