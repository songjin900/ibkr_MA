from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

def place_order(symbol, action, quantity):
    contract = Stock(symbol, 'SMART', 'USD')
    order = MarketOrder(action.upper(), quantity)
    trade = ib.placeOrder(contract, order)
    return trade
