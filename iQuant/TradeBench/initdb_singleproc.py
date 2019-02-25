import tushare as ts
import sqlalchemy as sa
import multiprocessing as mp
import pandas as pd
import datetime as dt


class InitMktProc(mp.Process):
    def __init__(self, flag, **kwargs):
        mp.Process.__init__(self)
        #
        self.eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
        tmp = pd.read_sql_table(table_name='stock_basic', con=self.eng, columns=('ts_code', 'list_status'))
        tmp = tmp[tmp.list_status == 'L']['ts_code']
        self.tscode = tmp.tolist()
        #
        tmp = pd.read_sql_table(table_name='trade_cal', con=self.eng, columns=('cal_date', 'is_open'))
        tmp = tmp[tmp.is_open == 1]['cal_date']
        self.cal = tmp.tolist()
        #
        if flag == 'moneyflow':
            self.flag = 'moneyflow'
        elif flag == 'hsgt_top10':
            self.flag = 'hsgt_top10'
        elif flag == 'ggt_top10':
            self.flag = 'ggt_top10'
        elif flag == 'top10_holders':
            self.flag = 'top10_holders'
        elif flag == 'top10_floatholders':
            self.flag = 'top10_floatholders'
        else:
            return
        #
        self.pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
        #
        if 'mkt' in kwargs:
            self.mkt = kwargs.get('mkt')


    def run(self):
        if self.flag == 'moneyflow':
            tN = len(self.cal)
            step = 60
            for i in range(int(tN/step)):
                df = self.pro.moneyflow_hsgt(start_date=self.cal[i * step], end_date=self.cal[(i + 1) * step - 1])
                df.to_sql(name='moneyflow_hsgt', con=self.eng, if_exists='append', index=False)
            #
            df = self.pro.moneyflow_hsgt(start_date=self.cal[int(tN/step) * step], end_date=self.cal[-1])
            df.to_sql(name='moneyflow_hsgt', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'hsgt_top10':
            if self.mkt is not None:
                for c in self.cal:
                    df = self.pro.hsgt_top10(trade_date=c, market_type=self.mkt)
                    df.to_sql(name='hsgt_top10', con=self.eng, if_exists='append', index=False)
            else:
                print('error! market type is none.')
        elif self.flag == 'ggt_top10':
            if self.mkt is not None:
                for c in self.cal:
                    df = self.pro.ggt_top10(trade_date=c, market_type=self.mkt)
                    df.to_sql(name='ggt_top10', con=self.eng, if_exists='append', index=False)
            else:
                print('error! market type is none.')
        elif self.flag == 'top10_holders':
            for c in self.tscode:
                df = self.pro.top10_holders(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='top10_holders', con=self.eng, if_exists='append', index=False)
                while len(df) == 100:
                    df = self.pro.top10_holders(ts_code=c, start_date=self.cal[0], end_date=df['end_date'][99])
                    df.to_sql(name='top10_holders', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'top10_floatholders':
            for c in self.tscode:
                df = self.pro.top10_floatholders(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='top10_floatholders', con=self.eng, if_exists='append', index=False)
                while len(df) == 100:
                    df = self.pro.top10_floatholders(ts_code=c, start_date=self.cal[0], end_date=df['end_date'][99])
                    df.to_sql(name='top10_floatholders', con=self.eng, if_exists='append', index=False)
        else:
            print('command:')
            print('%s moneyflow/hsgt_top10/ggt_top10/top10_holders' % __file__)


if __name__ == '__main__':
    bng = dt.datetime.now()
    #
    plst = []
    plst.append(InitMktProc(flag='moneyflow'))
    plst.append(InitMktProc(flag='hsgt_top10', mkt='1'))
    plst.append(InitMktProc(flag='hsgt_top10', mkt='3'))
    plst.append(InitMktProc(flag='ggt_top10', mkt= '2'))
    plst.append(InitMktProc(flag='ggt_top10', mkt='4'))
    plst.append(InitMktProc(flag='top10_holders'))
    #
    for p in plst:
        p.start()

    for p in plst:
        p.join()
    #
    print('%s run %0.2f seconds.' % (__file__, (dt.datetime.now() - bng).total_seconds()))
