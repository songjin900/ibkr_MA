from config import STOCK_LIST, POSITION_SIZE
from strategy import check_entry, check_exit
from broker import place_order, ib
from logger import log_trade
from notifier import send_discord_message
from ib_insync import *
from datetime import datetime
import time


active_positions = {}

def is_market_open():
    now = datetime.now().time()
    return now >= datetime.strptime("09:30", "%H:%M").time() and \
           now <= datetime.strptime("16:00", "%H:%M").time()


send_discord_message("✅ 프로그램 돌아가기 시작! 🎉")

while not is_market_open():
    now = datetime.now().time()
    if now >= datetime.strptime("09:25", "%H:%M").time():
        send_discord_message("5분안에 시작~")
        time.sleep(60)

send_discord_message("✅ 마켓 입장장 🎉")

while is_market_open():

    for symbol in STOCK_LIST:
        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)

        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='10 D',
            barSizeSetting='5 mins',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1,
            keepUpToDate=True
        )

        def on_update(bars, hasNewBar, symbol=symbol):
            print("in on_update function")
            if not hasNewBar: return
            df = util.df(bars)
            df['MA50'] = df['close'].rolling(50).mean()
            df['MA200'] = df['close'].rolling(200).mean()
            df['TP'] = (df['high'] + df['low'] + df['close']) / 3
            df['VWAP'] = (df['TP'] * df['volume']).cumsum() / df['volume'].cumsum()

            if symbol not in active_positions:
                if check_entry(df):
                    trade = place_order(symbol, 'BUY', POSITION_SIZE)
                    entry_price = df['close'].iloc[-1]
                    active_positions[symbol] = entry_price
                    msg = f"✅ 매수: {symbol} @ {entry_price}"
                    log_trade('BUY', symbol, entry_price, '골든크로스 + VWAP')
                    send_discord_message(msg)

            else:
                current_price = df['close'].iloc[-1]
                entry_price = active_positions[symbol]
                exit_reason = check_exit(entry_price, current_price)

                if exit_reason:
                    trade = place_order(symbol, 'SELL', POSITION_SIZE)
                    msg = f"🚨 매도: {symbol} @ {current_price} ({exit_reason})"
                    log_trade('SELL', symbol, current_price, exit_reason)
                    send_discord_message(msg)
                    del active_positions[symbol]

        bars.updateEvent += on_update

    time.sleep(60)

ib.run()
