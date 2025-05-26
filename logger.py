import csv
from datetime import datetime

def log_trade(action, symbol, price, reason):
    with open('log/trades.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), symbol, action, price, reason])