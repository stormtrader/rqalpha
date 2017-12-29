from rqalpha.api import *

import talib


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.s1 = "601766.XSHG"

    context.sma_s1_num = 5
    context.sma_s2_num = 10
    context.sma_s3_num = 20
    context.sma_s4_num = 30
    context.sma_l1_num = 60
    context.sma_l2_num = 89
    context.sma_l3_num = 120
    context.sma_l4_num = 250


def climb_up_long(sma_l1, sma_l2,sma_l3, sma_l4):
    # 最近10天内长期均线向上,并且是发散的
    for i in range(-10, -1):
        if sma_l1[i] < sma_l2[i] or sma_l2[i] < sma_l3[i] or sma_l3[i] < sma_l4[i]:
            return False

    return True

def check_price_near_by(price, sma_price):
    if price < sma_price:
        return True
    elif (price - sma_price)/sma_price < 0.005 :
        return True
    else:
        return False

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑
    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！

    # 因为策略需要用到均线，所以需要读取历史数据
    # 获取各种曲线的均线5， 10 ，20， 30， 60， 89， 120， 250

    prices = history_bars(context.s1, context.sma_l4_num+1, '1d', 'close')

    # 使用talib计算长短两根均线，均线以array的格式表达
    sma_s1 = talib.SMA(prices, context.sma_s1_num)
    sma_s2 = talib.SMA(prices, context.sma_s2_num)
    sma_s3 = talib.SMA(prices, context.sma_s3_num)
    sma_s4 = talib.SMA(prices, context.sma_s4_num)
    sma_l1 = talib.SMA(prices, context.sma_l1_num)
    sma_l2 = talib.SMA(prices, context.sma_l2_num)
    sma_l3 = talib.SMA(prices, context.sma_l3_num)
    sma_l4 = talib.SMA(prices, context.sma_l4_num)

    #展现均线
    plot("sma_s1 avg", sma_s1[-1])
    plot("sma_s2 avg", sma_s2[-1])
    plot("sma_s3 avg", sma_s3[-1])
    plot("sma_s4 avg", sma_s4[-1])
    plot("sma_l1 avg", sma_l1[-1])
    plot("sma_l2 avg", sma_l2[-1])
    plot("sma_l3 avg", sma_l3[-1])
    plot("sma_l4 avg", sma_l4[-1])

    # 计算现在portfolio中股票的仓位
    cur_position = context.portfolio.positions[context.s1].quantity
    # 计算现在portfolio中的现金可以购买多少股票
    shares = context.portfolio.cash / bar_dict[context.s1].close



    #买入策略：1. 长期均线往上；2. 上一个5日线的顶峰是近3个月最高,并且 顶峰前期是发散的；3. 今天的股价跌到60线附近；
    sma_util = SMAUtil(sma_l1)

    if climb_up_long(sma_l1, sma_l2, sma_l3, sma_l4) and sma_util.check_nearest_top()  \
        and check_price_near_by(bar_dict[context.s1].low, sma_l1[-1]):
        order_shares(context.s1, shares)

    #卖出策略：1. 至少持有5天；2. 止损卖出




    # 如果短均线从上往下跌破长均线，也就是在目前的bar短线平均值低于长线平均值，而上一个bar的短线平均值高于长线平均值
    if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0 and cur_position > 0:
        # 进行清仓
        order_target_value(context.s1, 0)

    # 如果短均线从下往上突破长均线，为入场信号
    if short_avg[-1] - long_avg[-1] > 0 and short_avg[-2] - long_avg[-2] < 0:
        # 满仓入股
        order_shares(context.s1, shares)
