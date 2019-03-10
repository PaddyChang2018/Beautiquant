import tushare as ts
import sqlalchemy as sa
import multiprocessing as mp
import pandas as pd
import os
import datetime as dt

class InitDB_Proc(mp.Process):
    '''
    每个类的实例都是一个进程
    '''
    def __init__(self, flag, **kwargs):
        '''
        初始化函数：获取基于base类创建的表格中的数据，而获取新的数据
        参数：
        flag：获取数据的类型标记
        connlmt:没分钟连接次数限制
        rcdlmt:每次获得数据记录条数限制
        ascend:升序为1,默认为降序0
        '''
        # 调用父类进程类构造函数
        mp.Process.__init__(self)
        # 初始化类基本成员参数
        self.flag = flag
        self.pro = ts.pro_api('349801780da0176efd38f64c3939020b3c2b3e6acbb6ac44ba627598')
        self.eng = sa.create_engine('mysql+pymysql://root:billchang106@127.0.0.1:3306/financial?charset=utf8mb4')
        #
        by_tscode = ['income','balance','cashflow','forecast','express','fina_indicator','audit','mainbz',
                     'pledge_stat','pledge_detail']
        by_cal = ['margin','margin_detail','top_list','top_inst','repurchase','index_daily','index_weight',
                  'index_dailybasic','express','fina_indicator','cashflow','mainbz','balance','forecast','income']
        by_idx = ['index_daily', 'index_weight', 'index_dailybasic']
        #
        if self.flag in by_tscode:
            # 如果按股票代码获取数据，则先获取股票代码列表
            tmp = pd.read_sql_table(table_name='stock_basic', con=self.eng, columns=('ts_code', 'list_status'))
            tmp = tmp[tmp.list_status == 'L']['ts_code']
            self.tscode = tmp.tolist()
        #
        if self.flag in by_cal:
            # 如果按交易日历获取数据，则先获取交易日历列表
            tmp = pd.read_sql_table(table_name='trade_cal', con=self.eng, columns=('cal_date', 'is_open'))
            tmp = tmp[tmp.is_open == 1]['cal_date']
            self.cal = tmp.tolist()
        #
        if self.flag in by_idx:
            tmp = pd.read_sql_table(table_name='index_basic', con=self.eng, columns=('ts_code',))
            self.idx = tmp['ts_code'].tolist()
        # 按获取各种数据类型flag进行区分
        if self.flag == 'income':
            # 利润表
            self.file = 'income.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 80
        elif self.flag == 'balance':
            # 资产负债表
            self.file = 'balance.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 80
        elif self.flag == 'cashflow':
            # 现金流量表
            self.file = 'cashflow.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 80
        elif self.flag == 'forecast':
            # 业绩预告
            self.file = 'forecast.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 60
        elif self.flag == 'express':
            # 业绩快报
            self.file = 'express.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 60
        elif self.flag == 'fina_indicator':
            # 财务指标数据
            self.file = 'fina_indicator.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 80
        elif self.flag == 'audit':
            # 财务审计意见
            self.file = 'audit.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 60
        elif self.flag == 'mainbz':
            # 主营业务构成
            self.file = 'mainbz.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 60
        elif self.flag == 'margin':
            # 融资融券交易汇总
            self.file = 'margin.rcd'
            self.tN = len(self.cal)
            self.connlmt = 80
        elif self.flag == 'margin_detail':
            # 融资融券交易明细
            self.file = 'margin_detail.rcd'
            self.tN = len(self.cal)
            self.connlmt = 80
        elif self.flag == 'top_list':
            # 龙虎榜每日明细
            self.file = 'top_list.rcd'
            self.tN = len(self.cal)
            self.connlmt = 80
        elif self.flag == 'top_inst':
            # 龙虎榜机构明细
            self.file = 'top_inst.rcd'
            self.tN = len(self.cal)
            self.connlmt = 60
        elif self.flag == 'pledge_stat':
            # 股权质押统计数据
            self.file = 'pledge_stat.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 50
        elif self.flag == 'pledge_detail':
            # 股权质押明细
            self.file = 'pledge_detail.rcd'
            self.tN = len(self.tscode)
            self.connlmt = 50
        elif self.flag == 'repurchase':
            # 股票回购
            self.file = 'repurchase.rcd'
            self.connlmt = 20
            self.rcdlmt = 2000
        elif self.flag == 'concept_detail':
            # 概念股分类明细数据
            self.file = 'concept_detail.rcd'
            self.tN = len(pd.read_sql_table(table_name='concept', con=self.eng))
            self.connlmt = 60
        elif self.flag == 'index_daily':
            # 指数日线行情
            self.file = 'index_daily.rcd'
            self.tN = len(self.idx)
            self.connlmt = 100
            self.rcdlmt = 1800
        elif self.flag == 'index_weight':
            # 获取各类指数成分和权重，月度数据
            self.file = 'index_weight.rcd'
            self.tN = len(self.idx)
            self.connlmt = 70
            self.rcdlmt = 3000
        elif self.flag == 'index_dailybasic':
            # 大盘指数每日指标
            # 目前只提供上证综指，深证成指，上证50，中证500，中小板指，创业板指的每日指标数据
            self.file = 'index_dailybasic.rcd'
            self.tN = len(self.cal)
            self.connlmt = 100
        else:
            return
        #
        if 'connlmt' in kwargs:
            # 如果在构造函数中有connlmt参数
            if kwargs['connlmt'] > 0:
                # 如果每分钟连接数有限制
                self.connlmt = kwargs['connlmt']
        #
        if 'rcdlmt' in kwargs:
            # 如果在构造函数中有rcdlmt参数
            if kwargs['rcdlmt'] > 0:
                # 如果每次获取记录数有限制
                self.rcdlmt = kwargs['rcdlmt']
        #
        try:
            self.file   # 用文件成员变量判断是否需要记录获取数据中间节点
        except AttributeError:
            pass
        else:
            if os.access(self.file, os.R_OK):
                # 如果记录文件可读，即将节点记录读到self.cN中
                with open(self.file, 'r') as f:
                    c = f.readline()
                if self.flag not in {'repurchase'}:
                    # 如果flag是常规的，则将从文件读到的节点记录转化成整数，否则将以字符串方式存储在self.cN中
                    self.cN = int(c)
                else:
                    self.cN = c
            else:
                # 如果记录文件不可读，则节点记录数为0
                self.cN = 0

    def __str__(self):
        return 'InitDB_Proc(%s)' % self.flag

    def run(self):
        # 判断每分钟连接数connlmt成员是否存在
        try:
            self.connlmt
        except AttributeError:
            pass
        else:
            if self.connlmt > 0:
                # 如果每分钟连接数受限制，需将中断节点记录进文件
                if self.flag not in {'repurchase'}:
                    # 如果数据类型是普通类型，self.cN是整数的情况下
                    if self.cN >= self.tN:
                        return
                    elif self.cN + self.connlmt >= self.tN:
                        endidx = self.tN
                    else:
                        endidx = self.cN + self.connlmt
        # 按数据类型标识区分
        if self.flag == 'income':
            # 利润表
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.income(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='income', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'balance':
            # 资产负债表
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.balancesheet(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='balance', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'cashflow':
            # 现金流量表
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.cashflow(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='cashflow', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'forecast':
            # 业绩预告
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.forecast(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='forecast', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'express':
            # 业绩快报
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.express(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='express', con=self.eng, if_exists='append', index=False)
            self.cN = endidx
        elif self.flag == 'fina_indicator':
            # 财务指标数据
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.fina_indicator(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='fina_indicator', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'audit':
            # 财务审计意见
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.fina_audit(ts_code=c)
                df.to_sql(name='audit', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'mainbz':
            # 主营业务构成
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.fina_mainbz(ts_code=c, start_date=self.cal[0], end_date=self.cal[-1])
                df.to_sql(name='mainbz', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'margin':
            # 融资融券交易汇总
            for c in self.cal[self.cN:endidx]:
                df = self.pro.margin(trade_date=c)
                df.to_sql(name='margin', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'margin_detail':
            # 融资融券交易明细
            for c in self.cal[self.cN:endidx]:
                df = self.pro.margin_detail(trade_date=c)
                df.to_sql(name='margin_detail', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'top_list':
            # 龙虎榜每日明细
            for c in self.cal[self.cN:endidx]:
                df = self.pro.top_list(trade_date=c)
                df.to_sql(name='top_list', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'top_inst':
            # 龙虎榜机构明细
            for c in self.cal[self.cN:endidx]:
                df = self.pro.top_inst(trade_date=c)
                df.to_sql(name='top_inst', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'pledge_stat':
            # 股权质押统计数据
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.pledge_stat(ts_code=c)
                df.to_sql(name='pledge_stat', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'pledge_detail':
            # 股权质押明细
            for c in self.tscode[self.cN:endidx]:
                df = self.pro.pledge_detail(ts_code=c)
                df.to_sql(name='pledge_detail', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'repurchase':
            # 股票回购
            if self.cN == 0:
                self.cN = self.cal[-1]
            for i in range(self.connlmt):
                df = self.pro.repurchase(start_date=self.cal[0], end_date=self.cN)
                df.to_sql(name='repurchase', con=self.eng, if_exists='append', index=False)
                self.cN = df.iloc[-1]['ann_date']
                if len(df) < self.rcdlmt:
                    self.cN = None
                    break
        elif self.flag == 'concept':
            # 概念股分类
            df = self.pro.concept(src='ts')
            df.to_sql(name='concept', con=self.eng, if_exists='replace', index=False)
        elif self.flag == 'concept_detail':
            # 获取概念股分类明细数据
            for i in range(self.cN, endidx):
                df = self.pro.concept_detail(id=i.__str__())
                df.to_sql(name='concept_detail', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'index_basic':
            # 获取指数基础信息
            mkt = {'CICC', 'CNI', 'CSI', 'MSCI', 'SSE', 'OTH', 'SZSE', 'SW'}
            for m in mkt:
                df = self.pro.index_basic(market=m)
                df.to_sql(name='index_basic', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'index_daily':
            # 获取指数每日行情
            for i in self.idx[self.cN:endidx]:
                df = self.pro.index_daily(ts_code=i, start_date= self.cal[0], end_date=self.cal[-1])
                if not df.empty:
                    df.to_sql(name='index_daily', con=self.eng, if_exists='append', index=False)
                while len(df) >= self.rcdlmt:
                    df = self.pro.index_daily(ts_code=i, start_date=self.cal[0], end_date=df.iloc[-1]['trade_date'])
                    df.to_sql(name='index_daily', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'index_weight':
            # 获取各类指数成分和权重，月度数据
            for i in self.idx[self.cN:endidx]:
                df = self.pro.index_weight(ts_code=i, start_date= self.cal[0], end_date=self.cal[-1])
                if not df.empty:
                    df.to_sql(name='index_weight', con=self.eng, if_exists='append', index=False)
                while len(df) >= self.rcdlmt:
                    df = self.pro.index_weight(ts_code=i, start_date=self.cal[0], end_date=df.iloc[-1]['trade_date'])
                    df.to_sql(name='index_weight', con=self.eng, if_exists='append', index=False)
        elif self.flag == 'index_dailybasic':
            # 大盘指数每日指标
            # 目前只提供上证综指，深证成指，上证50，中证500，中小板指，创业板指的每日指标数据
            for c in self.cal[self.cN:endidx]:
                df = self.pro.index_dailybasic(trade_date=c)
                df.to_sql(name='index_dailybasic', con=self.eng, if_exists='append', index=False)
        else:
            return
        #
        # 如果每分钟连接数受限，则将此次节点记录写回文件
        try:
            self.connlmt
        except AttributeError:
            pass
        else:
            if self.connlmt > 0:
                # 如果每分钟连接数受限制，需将中断节点记录进文件
                if self.flag not in {'repurchase'}:
                    # 常规情况
                    self.cN = endidx
                # 将中断节点信息写进记录文件
                with open(self.file, 'w') as f:
                    f.writelines(str(self.cN) + '\n')

if __name__ == '__main__':
    bngtime = dt.datetime.now()
    plst = []
    #
    plst.append(InitDB_Proc(flag='income'))
    plst.append(InitDB_Proc(flag='balance'))
    plst.append(InitDB_Proc(flag='cashflow'))
    plst.append(InitDB_Proc(flag='forecast'))
    plst.append(InitDB_Proc(flag='express'))
    plst.append(InitDB_Proc(flag='fina_indicator'))
    plst.append(InitDB_Proc(flag='audit'))
    plst.append(InitDB_Proc(flag='mainbz'))
    plst.append(InitDB_Proc(flag='margin'))
    plst.append(InitDB_Proc(flag='margin_detail'))
    plst.append(InitDB_Proc(flag='top_list'))
    plst.append(InitDB_Proc(flag='top_inst'))
    plst.append(InitDB_Proc(flag='pledge_stat'))
    plst.append(InitDB_Proc(flag='pledge_detail'))
    plst.append(InitDB_Proc(flag='repurchase'))
    plst.append(InitDB_Proc(flag='concept'))
    #
    for p in plst:
        p.start()
    #
    for p in plst:
        p.join()
    #
    print('%s run %0.2f seconds.' % (__file__, (dt.datetime.now() - bngtime).total_seconds()))