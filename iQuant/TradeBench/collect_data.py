import tushare as ts
import sqlalchemy as sa
import datetime as dt

def datefeed_tushare(dataname=None, db_exists='append', **kwargs):
    try:
        pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
        eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
    except Exception as e:
        print(e)

    if dataname == 'stock_basic':
        df = pro.stock_basic(**kwargs)    # **kwargs : list_status='L'上市/'D'退市/'P'暂停上市
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    elif dataname == 'trade_cal':
        df = pro.trade_cal(is_open=1, **kwargs)    # **kwargs : start_date='20180101', end_date='20181231'
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    elif dataname == 'hs_const':
        df = pro.hs_const(hs_type='SH')
        df.to_sql(name=dataname, con=eng, if_exists='replace', index=False)
        df = pro.hs_const(hs_type='SZ')
        df.to_sql(name=dataname, con=eng, if_exists='append', index=False)
    elif dataname == 'stock_company':
        df = pro.stock_company(exchange='SSE',
                               fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,'
                                      'city,introduction,website,email,office,employees,main_business,business_scope')
        df.to_sql(name=dataname, con=eng, if_exists='replace', index=False)
        df = pro.stock_company(exchange='SZSE',
                               fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,'
                                      'city,introduction,website,email,office,employees,main_business,business_scope')
        df.to_sql(name=dataname, con=eng, if_exists='append', index=False)
    elif dataname == 'new_share':
        #单次最大2000条，总量不限制
        df = pro.new_share(**kwargs)           # **kwargs : start_date = '20180901', end_date = '20181018'
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    elif dataname == 'daily':
        # 每分钟内最多调取200次，超过5000积分无限制
        df = pro.daily(**kwargs)
        # **kwargs : trade_date='20190308' or ts_code='000001.SZ', start_date='20180701', end_date='20180718'
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    elif dataname == 'weekly':
        # 单次最大3700，总量不限制
        df = pro.weekly(**kwargs)
        # **kwargs : trade_date='20181123' or ts_code='000001.SZ', start_date='20180101', end_date='20181101'
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    elif dataname == 'monthly':
        # 单次最大3700，总量不限制
        df = pro.monthly(**kwargs)
        # **kwargs : trade_date='20181031' or ts_code='000001.SZ', start_date='20180101', end_date='20181101'
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    elif dataname == 'qianfuquan':
        df = ts.pro_bar(pro_api=pro, adj='qfq', **kwargs)
        # **kwargs : ts_code='000001.SZ', start_date='20180101', end_date='20181011'
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    elif dataname == 'houfuquan':
        df = ts.pro_bar(pro_api=pro, adj='hfq', **kwargs)
        # **kwargs : ts_code='000001.SZ', start_date='20180101', end_date='20181011'
        df.to_sql(name=dataname, con=eng, if_exists=db_exists, index=False)
    else:
        print('no %s data!' % dataname)


if __name__=="__main__":
    bng = dt.datetime.now()
    #datefeed_tushare('stock_basic', list_status='L')
    #datefeed_tushare('trade_cal', start_date='20160101', end_date='20190308')
    #datefeed_tushare('hs_const')
    datefeed_tushare('stock_company')
    print("%s run %0.2f seconds." % (__file__, (dt.datetime.now() - bng).total_seconds()))
