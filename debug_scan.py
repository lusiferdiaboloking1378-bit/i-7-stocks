import pandas as pd
import yfinance as yf
import ta
import numpy as np

ACTIVE_WATCHLIST = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'INFOSYS': 'INFY.NS',
    'TATAMOTORS': '500570.BO',
    'SBIN': 'SBIN.NS',
    'ZOMATO': 'ZOMATO.NS',
    'ITC': 'ITC.NS',
    'JIOFIN': 'JIOFIN.NS',
    'TATASTEEL': 'TATASTEEL.NS',
    'HAL': 'HAL.NS',
}

# mimic app logic
interval = '1d'
period = '6mo'
sym_list = list(ACTIVE_WATCHLIST.values())
data = yf.download(sym_list, period=period, interval=interval, group_by='ticker', threads=True, progress=False)
print('downloaded', type(data), data.shape)
print('columns names', data.columns.names)
print('first cols', data.columns[:10])
results = []
for idx, (name, sym) in enumerate(ACTIVE_WATCHLIST.items()):
    try:
        if isinstance(data, pd.DataFrame) and data.columns.nlevels > 1 and 'Ticker' in data.columns.names:
            if sym not in data.columns.get_level_values('Ticker'):
                print('skip missing', sym)
                continue
            df = data.xs(sym, level='Ticker', axis=1).copy()
        else:
            if sym not in data.columns:
                print('skip not in columns', sym)
                continue
            df = data.copy()
        df.dropna(subset=['Close'], inplace=True)
        if df.empty or len(df) < 20:
            print('skip short', sym, len(df))
            continue
        ltp = float(df['Close'].iloc[-1])
        print('accepted', sym, ltp)
        results.append(sym)
    except Exception as e:
        print('exception', sym, type(e).__name__, e)

print('results count', len(results))
