import pandas as pd

mid_type = ''
ratio = 0.2
interval = 1

# 변수 초기화
var = {
    'prevBidQty': 0,
    'prevAskQty': 0,
    'prevBidTop': 0,
    'prevAskTop': 0,
    'bidSideAdd': 0,
    'bidSideDelete': 0,
    'askSideAdd': 0,
    'askSideDelete': 0,
    'bidSideTrade': 0,
    'askSideTrade': 0,
    'bidSideFlip': 0,
    'askSideFlip': 0,
    'bidSideCount': 0,
    'askSideCount': 0,
    '_flag': True
}

decay = 0.9  # example decay factor

def cal_mid_price(gr_bid_level, gr_ask_level):
    if len(gr_bid_level) > 0 and len(gr_ask_level) > 0:
        bid_top_price = gr_bid_level.iloc[0].price
        ask_top_price = gr_ask_level.iloc[0].price
        mid_price = (bid_top_price + ask_top_price) * 0.5
        return mid_price
    else:
        print('Error: serious cal_mid_price')
        return -1

def cal_book_imbalance(gr_bid_level, gr_ask_level, mid_price, ratio=0.2, interval=1):
    if len(gr_bid_level) > 0 and len(gr_ask_level) > 0:
        quant_v_bid = gr_bid_level.quantity ** ratio
        price_v_bid = gr_bid_level.price * quant_v_bid

        quant_v_ask = gr_ask_level.quantity ** ratio
        price_v_ask = gr_ask_level.price * quant_v_ask

        askQty = quant_v_ask.sum()
        bidPx = price_v_bid.sum()
        bidQty = quant_v_bid.sum()
        askPx = price_v_ask.sum()

        book_price = (((askQty * bidPx) / bidQty) + ((bidQty * askPx) / askQty)) / (bidQty + askQty)
        book_imbalance = (book_price - mid_price) / interval

        return book_imbalance
    else:
        return -1

def cal_book_d_indicator(gr_bid_level, gr_ask_level, diff, var, ratio=0.2, decay=0.9):
    prevBidQty = var['prevBidQty']
    prevAskQty = var['prevAskQty']
    prevBidTop = var['prevBidTop']
    prevAskTop = var['prevAskTop']
    bidSideAdd = var['bidSideAdd']
    bidSideDelete = var['bidSideDelete']
    askSideAdd = var['askSideAdd']
    askSideDelete = var['askSideDelete']
    bidSideTrade = var['bidSideTrade']
    askSideTrade = var['askSideTrade']
    bidSideFlip = var['bidSideFlip']
    askSideFlip = var['askSideFlip']
    bidSideCount = var['bidSideCount']
    askSideCount = var['askSideCount']

    curBidQty = gr_bid_level['quantity'].sum()
    curAskQty = gr_ask_level['quantity'].sum()
    curBidTop = gr_bid_level.iloc[0].price
    curAskTop = gr_ask_level.iloc[0].price

    if var['_flag']:
        var['prevBidQty'] = curBidQty
        var['prevAskQty'] = curAskQty
        var['prevBidTop'] = curBidTop
        var['prevAskTop'] = curAskTop
        var['_flag'] = False
        return 0.0

    if curBidQty > prevBidQty:
        bidSideAdd += 1
        bidSideCount += 1
    if curBidQty < prevBidQty:
        bidSideDelete += 1
        bidSideCount += 1
    if curAskQty > prevAskQty:
        askSideAdd += 1
        askSideCount += 1
    if curAskQty < prevAskQty:
        askSideDelete += 1
        askSideCount += 1

    if curBidTop < prevBidTop:
        bidSideFlip += 1
        bidSideCount += 1
    if curAskTop > prevAskTop:
        askSideFlip += 1
        askSideCount += 1

    _count_1, _count_0, _units_traded_1, _units_traded_0, _price_1, _price_0 = diff

    bidSideTrade += _count_1
    bidSideCount += _count_1

    askSideTrade += _count_0
    askSideCount += _count_0

    if bidSideCount == 0:
        bidSideCount = 1
    if askSideCount == 0:
        askSideCount = 1

    bidBookV = (-bidSideDelete + bidSideAdd - bidSideFlip) / (bidSideCount ** ratio)
    askBookV = (askSideDelete - askSideAdd + askSideFlip) / (askSideCount ** ratio)
    tradeV = (askSideTrade / askSideCount ** ratio) - (bidSideTrade / bidSideCount ** ratio)
    bookDIndicator = askBookV + bidBookV + tradeV

    var['bidSideCount'] = bidSideCount * decay
    var['askSideCount'] = askSideCount * decay
    var['bidSideAdd'] = bidSideAdd * decay
    var['bidSideDelete'] = bidSideDelete * decay
    var['askSideAdd'] = askSideAdd * decay
    var['askSideDelete'] = askSideDelete * decay
    var['bidSideTrade'] = bidSideTrade * decay
    var['askSideTrade'] = askSideTrade * decay
    var['bidSideFlip'] = bidSideFlip * decay
    var['askSideFlip'] = askSideFlip * decay

    var['prevBidQty'] = curBidQty
    var['prevAskQty'] = curAskQty
    var['prevBidTop'] = curBidTop
    var['prevAskTop'] = curAskTop

    return bookDIndicator

def cal_mid_price(gr_bid_level, gr_ask_level):

    if len(gr_bid_level) > 0 and len(gr_ask_level) > 0:
        bid_top_price = gr_bid_level.iloc[0].price
        ask_top_price = gr_ask_level.iloc[0].price
        mid_price = (bid_top_price + ask_top_price) * 0.5 
        return (mid_price)

    else:
        print ('Error: serious cal_mid_price')
        return (-1)
    

def cal_book_imbalance(gr_bid_level, gr_ask_level, mid_price, ratio=0.2, interval=1):
    if len(gr_bid_level) > 0 and len(gr_ask_level) > 0:
        quant_v_bid = gr_bid_level.quantity ** ratio
        price_v_bid = gr_bid_level.price * quant_v_bid

        quant_v_ask = gr_ask_level.quantity ** ratio
        price_v_ask = gr_ask_level.price * quant_v_ask

        askQty = quant_v_ask.sum()
        bidPx = price_v_bid.sum()
        bidQty = quant_v_bid.sum()
        askPx = price_v_ask.sum()

        book_price = (((askQty * bidPx) / bidQty) + ((bidQty * askPx) / askQty)) / (bidQty + askQty)
        book_imbalance = (book_price - mid_price) / interval

        return book_imbalance
    else:
        return -1

results=[]



df = pd.read_csv('feature3.csv').apply(pd.to_numeric,errors='ignore')
groups = df.groupby('timestamp')

for timestamp, gr_o in groups:
    gr_bid_level = gr_o[gr_o.type == 0]
    gr_ask_level = gr_o[gr_o.type == 1]
    mid_price = cal_mid_price(gr_bid_level, gr_ask_level)
    book_imbalance = cal_book_imbalance(gr_bid_level, gr_ask_level, mid_price)
    
    # Placeholder for diff, replace with actual logic
    diff = (0, 0, 0, 0, 0, 0)
    
    book_d_indicator = cal_book_d_indicator(gr_bid_level, gr_ask_level, diff, var)
    
    results.append({'timestamp': timestamp, 'mid_price': mid_price, 'book_imbalance': book_imbalance, 'book_d_indicator': book_d_indicator})

results_df = pd.DataFrame(results)
results_df.to_csv('calculated_mid_prices_and_imbalances.csv', index=False)


    # 다른 특성 계산
    # csv에 쓰기

