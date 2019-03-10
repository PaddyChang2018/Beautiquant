import multiprocessing as mp
from .collect_data import *

def get_basic_data_from_tushare():
    datefeed_tushare('stock_basic', list_status='L')
    datefeed_tushare('trade_cal', start_date='20160101', end_date='20190308')
    datefeed_tushare('hs_const')
    datefeed_tushare('stock_company')

if __name__=="__main__":
    pl = mp.Pool(processes=mp.cpu_count())
    pl.apply_async(func=get_basic_data_from_tushare)
    pl.close()
    pl.join()
