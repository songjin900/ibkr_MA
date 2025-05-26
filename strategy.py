def check_entry(df):
    # 골든크로스 + VWAP 위 조건
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    golden = prev['MA50'] <= prev['MA200'] and latest['MA50'] > latest['MA200']
    above_vwap = latest['close'] > latest['VWAP']
    return golden and above_vwap

def check_exit(entry_price, current_price):
    change = (current_price - entry_price) / entry_price
    if change <= -0.02:
        return 'stop_loss'
    elif change >= 0.05:
        return 'take_profit'
    return None
