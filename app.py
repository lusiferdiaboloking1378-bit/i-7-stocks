import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import os
import csv
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="i-7 Tech | Dashboard", page_icon="⚡", layout="wide")

# --- FREE AUTO-REFRESH (removed) ---
# Auto-refresh behavior removed per user request.

# --- CINEMATIC CYBERPUNK CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

html, body, .stApp { background-color: #0E1117 !important; color: #E0E0E0 !important; }
div[data-testid="stSidebar"] { background-color: #12141A !important; border-right: 1px solid #1F2230; }
div[data-testid="stSidebar"] label, div[data-testid="stSidebar"] p { color: #AAAAAA !important; }
h1, h2, h3, h4 { font-family: 'Share Tech Mono', monospace !important; color: #FFFFFF !important; }

/* Neon Scan Button */
.stButton > button {
    background: transparent !important; border: 2px solid #00FF66 !important;
    color: #00FF66 !important; font-family: 'Share Tech Mono', monospace !important;
    font-size: 16px !important; letter-spacing: 2px; padding: 12px !important;
    border-radius: 4px !important; transition: all 0.2s ease;
}
.stButton > button:hover { background: #00FF66 !important; color: #0E1117 !important; box-shadow: 0 0 20px rgba(0,255,102,0.5); }

/* Number Input */
div[data-testid="stNumberInput"] input {
    background-color: #1A1D24 !important; color: #00FF66 !important;
    border: 1px solid #00FF66 !important; border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important; font-size: 18px !important;
}

/* Metric */
div[data-testid="stMetricValue"] { color: #00FF66 !important; font-weight: bold !important; }
div[data-testid="stMetricLabel"] { color: #888888 !important; font-size: 12px !important; text-transform: uppercase; }

/* Progress bar */
.stProgress > div > div > div { background-color: #00FF66 !important; }

/* Gauge Card */
.gauge-card {
    background: #1A1D24; border: 2px solid #6200EE;
    border-radius: 16px; padding: 28px 20px; text-align: center;
    box-shadow: 0 0 30px rgba(98,0,238,0.2); margin-bottom: 16px;
}
.gauge-ring {
    width: 130px; height: 130px; border-radius: 50%;
    background: conic-gradient(#6200EE var(--pct), #2A2D37 var(--pct));
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 12px; box-shadow: 0 0 20px rgba(98,0,238,0.4);
}
.gauge-inner {
    width: 100px; height: 100px; border-radius: 50%; background: #1A1D24;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.gauge-val { font-size: 24px; font-weight: bold; color: #FFFFFF; font-family: monospace; }
.gauge-sub { font-size: 9px; color: #888; text-transform: uppercase; letter-spacing: 1px; }

/* Mini metric cards */
.mini-card {
    background: #1A1D24; border: 1px solid #2A2D37; border-radius: 10px;
    padding: 14px 10px; text-align: center; margin-bottom: 10px;
}
.mini-card .label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.mini-card .value { font-size: 20px; font-weight: bold; color: #FFFFFF; font-family: monospace; }

/* Signal rows */
.signal-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #1A1D24; border: 1px solid #222; border-radius: 10px;
    padding: 12px 16px; margin-bottom: 8px;
}
.badge-buy { background: #00FF66; color: #0E1117; padding: 4px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; }
.badge-hold { background: #FFC107; color: #0E1117; padding: 4px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; }
.badge-sell { background: #FF3366; color: #FFFFFF; padding: 4px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; }

/* Radio options styled as signal cards (matches screenshot exactly) */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div > label {
    background: #1A1D24 !important;
    border: 1px solid #222 !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
    cursor: pointer !important;
    color: #FFFFFF !important;
    font-size: 14px !important;
    font-family: 'Rajdhani', sans-serif !important;
    display: flex !important;
    align-items: center !important;
    transition: border-color 0.15s ease;
    width: 100% !important;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: #6200EE !important;
    box-shadow: 0 0 8px rgba(98,0,238,0.25) !important;
}
div[data-testid="stRadio"] > div > label[data-testid*="selected"],
div[data-testid="stRadio"] > div > label:has(input:checked) {
    border-color: #6200EE !important;
    box-shadow: 0 0 12px rgba(98,0,238,0.3) !important;
    background: #1F2230 !important;
}

/* Footer */
.footer-cta {
    background: #12141A; border-left: 4px solid #00FF66;
    padding: 18px 24px; margin-top: 40px; border-radius: 6px;
    font-family: monospace; font-size: 14px; color: #CCCCCC;
}

/* Tabs */
div[data-testid="stTabs"] button { color: #888888 !important; font-family: monospace !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #FFFFFF !important; border-bottom: 2px solid #6200EE !important; }

/* Mobile / compact screen layout */
@media (max-width: 900px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 0.75rem !important;
    }
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 0.5rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    .gauge-card {
        padding: 18px 12px;
    }
    .mini-card {
        padding: 10px 8px;
    }
    .signal-row {
        padding: 10px 12px;
    }
}

</style>
""", unsafe_allow_html=True)

# ===================================================================
# WATCHLIST
# ===================================================================
ACTIVE_WATCHLIST = {
    'RELIANCE':   'RELIANCE.NS',
    'TCS':        'TCS.NS',
    'INFOSYS':    'INFY.NS',
    'TATAMOTORS': '500570.BO',   # BSE fallback — NSE data unreliable
    'SBIN':       'SBIN.NS',
    'ZOMATO':     'ZOMATO.NS',
    'ITC':        'ITC.NS',
    'JIOFIN':     'JIOFIN.NS',
    'TATASTEEL':  'TATASTEEL.NS',
    'HAL':        'HAL.NS',
}

POSITIVE_WORDS = ['profit','growth','rise','surge','deal','order','dividend','buy','upgrade','record']
NEGATIVE_WORDS = ['loss','fall','drop','slump','fine','scam','investigation','sebi','decline','resign']

@st.cache_data(show_spinner=False, ttl=180)
def fetch_sentiment(sym):
    try:
        tkr = yf.Ticker(sym)
        news = (tkr.news or [])[:3]
        score = 0.0
        for item in news:
            title = ''
            if isinstance(item, dict):
                title = item.get('title', item.get('content', {}).get('title', '')).lower()
            for w in POSITIVE_WORDS: score += 0.3 if w in title else 0
            for w in NEGATIVE_WORDS: score -= 0.5 if w in title else 0
        return max(-1.0, min(1.0, score))
    except:
        return 0.0


def normalize_symbol(symbol):
    s = (symbol or '').strip().upper()
    if not s:
        return s
    if '.' in s or s.endswith(('NS', 'BO', 'NSE')):
        return s
    return f"{s}.NS"


def chunk_list(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def format_eta(seconds):
    if seconds <= 0:
        return 'estimating...'
    hours, rem = divmod(int(seconds), 3600)
    mins, secs = divmod(rem, 60)
    if hours:
        return f'{hours}h {mins}m'
    if mins:
        return f'{mins}m {secs}s'
    return f'{secs}s'


@st.cache_data(show_spinner=False, ttl=3600)
def get_company_position(sym):
    try:
        tkr = yf.Ticker(sym)
        info = tkr.info or {}
        market_cap = info.get('marketCap')
        pe_ratio = info.get('trailingPE')
        debt_to_equity = info.get('debtToEquity')
        revenue_growth = info.get('revenueGrowth')
        earnings_growth = info.get('earningsGrowth')
        profit_margins = info.get('profitMargins')
        return {
            'market_cap': market_cap,
            'pe_ratio': pe_ratio,
            'debt_to_equity': debt_to_equity,
            'revenue_growth': revenue_growth,
            'earnings_growth': earnings_growth,
            'profit_margins': profit_margins,
        }
    except Exception:
        return {
            'market_cap': None,
            'pe_ratio': None,
            'debt_to_equity': None,
            'revenue_growth': None,
            'earnings_growth': None,
            'profit_margins': None,
        }


@st.cache_data(show_spinner=False, ttl=60)
def get_live_quote(sym):
    try:
        tkr = yf.Ticker(sym)
        q = tkr.fast_info or {}
        price = getattr(q, 'last_price', None)
        if price is None:
            hist = tkr.history(period='2d', interval='1d')
            if not hist.empty:
                price = float(hist['Close'].iloc[-1])
        change = getattr(q, 'last_price', None)
        return {
            'price': float(price) if price is not None else None,
            'change': None,
        }
    except Exception:
        return {'price': None, 'change': None}


def build_stock_recommendation(name, sym, df, total_capital, trading_style):
    if df is None or df.empty or len(df) < 20:
        return {
            'eligible_status': '❌ Not ideal',
            'eligibility_note': 'Not enough historical data to rate this stock.',
            'eligibility_score': 0,
            'trade_type': 'Avoid',
            'trade_reason': 'Avoid this stock until enough data is available.'
        }

    ltp = float(df['Close'].iloc[-1])
    qty = int(np.floor(total_capital / (ltp + 20)))
    O, H, L, C = df['Open'].values, df['High'].values, df['Low'].values, df['Close'].values
    body = abs(C[-1] - O[-1])
    lower_shadow = min(O[-1], C[-1]) - L[-1]
    upper_shadow = H[-1] - max(O[-1], C[-1])
    is_hammer = (body > 0) and (lower_shadow >= 2 * body) and (upper_shadow <= 0.2 * body)
    is_engulfing = len(C) > 1 and C[-1] > O[-1] and C[-2] < O[-2] and C[-1] >= O[-2] and O[-1] <= C[-2]

    close = df['Close']
    high_s = df['High']
    low_s = df['Low']
    ema_20 = float(ta.trend.EMAIndicator(close=close, window=20).ema_indicator().iloc[-1])
    ema_50 = float(ta.trend.EMAIndicator(close=close, window=50).ema_indicator().iloc[-1])
    rsi = float(ta.momentum.RSIIndicator(close=close, window=14).rsi().iloc[-1])
    macd_o = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
    macd_l = float(macd_o.macd().iloc[-1])
    macd_s_val = float(macd_o.macd_signal().iloc[-1])
    atr_v = float(ta.volatility.AverageTrueRange(high=high_s, low=low_s, close=close, window=14).average_true_range().iloc[-1])
    pct_chg = float(((C[-1] - C[-2]) / C[-2]) * 100) if len(C) > 1 else 0.0
    volume = float(df['Volume'].iloc[-1])
    avg_50 = float(df['Close'].tail(50).mean())
    below_avg = ltp < avg_50
    avg_gap_pct = ((ltp - avg_50) / avg_50) * 100 if avg_50 > 0 else 0.0
    company_info = get_company_position(sym)
    market_cap = company_info.get('market_cap')
    pe_ratio = company_info.get('pe_ratio')
    debt_to_equity = company_info.get('debt_to_equity')
    revenue_growth = company_info.get('revenue_growth')
    earnings_growth = company_info.get('earnings_growth')
    profit_margins = company_info.get('profit_margins')

    # Enhanced accuracy indicators
    vol_avg_20 = float(df['Volume'].rolling(20).mean().iloc[-1]) if len(df) >= 20 else 0
    vol_spike = volume > 1.5 * vol_avg_20 if vol_avg_20 > 0 else False
    try:
        adx_v = float(ta.trend.ADXIndicator(high=high_s, low=low_s, close=close, window=14).adx().iloc[-1])
    except Exception:
        adx_v = 0.0
    high_52w = float(df['High'].tail(252).max())
    low_52w = float(df['Low'].tail(252).min())
    price_pct_from_low = (ltp - low_52w) / (high_52w - low_52w + 1e-9)
    near_52w_low = price_pct_from_low < 0.15
    try:
        weekly_close = df['Close'].resample('W').last().dropna()
        if len(weekly_close) >= 21:
            w_ema8 = float(ta.trend.EMAIndicator(close=weekly_close, window=8).ema_indicator().iloc[-1])
            w_ema21 = float(ta.trend.EMAIndicator(close=weekly_close, window=21).ema_indicator().iloc[-1])
            weekly_bullish = w_ema8 > w_ema21
        else:
            weekly_bullish = False
    except Exception:
        weekly_bullish = False
    try:
        bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
        bb_upper = float(bb.bollinger_hband().iloc[-1])
        bb_breakout = ltp > bb_upper * 0.98
    except Exception:
        bb_breakout = False

    eligibility_score = 0
    if qty > 0:
        eligibility_score += 20
    if ltp > ema_20:
        eligibility_score += 10
    if ema_20 > ema_50:
        eligibility_score += 15
    if abs(pct_chg) > 0.3:
        eligibility_score += 8
    if 45 <= rsi <= 70:
        eligibility_score += 12
    if macd_l > macd_s_val:
        eligibility_score += 12
    if volume > 1e6:
        eligibility_score += 8
    if is_hammer or is_engulfing:
        eligibility_score += 8
    if below_avg and avg_gap_pct < -5:
        eligibility_score -= 10
    if market_cap and market_cap > 1e10:
        eligibility_score += 8
    if pe_ratio and pe_ratio > 0 and pe_ratio < 40:
        eligibility_score += 5
    if debt_to_equity is not None and debt_to_equity < 1.0:
        eligibility_score += 5
    if revenue_growth is not None and revenue_growth > 0.05:
        eligibility_score += 5
    if earnings_growth is not None and earnings_growth > 0.05:
        eligibility_score += 5
    if profit_margins is not None and profit_margins > 0.05:
        eligibility_score += 5
    if vol_spike:
        eligibility_score += 10
    if not near_52w_low:
        eligibility_score += 5
    if weekly_bullish:
        eligibility_score += 12
    if adx_v > 20:
        eligibility_score += 8
    if bb_breakout:
        eligibility_score += 6

    if eligibility_score >= 70:
        eligibility_status = '✅ Eligible'
        eligibility_note = 'Good trend, liquidity and momentum make this stock investable.'
    elif eligibility_score >= 55:
        eligibility_status = '⚠️ Conditional'
        eligibility_note = 'The setup is decent, but size and stop-loss should be controlled.'
    else:
        eligibility_status = '❌ Not ideal'
        eligibility_note = 'Weak or choppy setup for fresh investment right now.'

    if debt_to_equity is not None and debt_to_equity > 1.5:
        risk_level = 'High'
        risk_note = 'The company carries heavy debt, so the business position looks fragile.'
    elif below_avg and avg_gap_pct < -10:
        risk_level = 'High'
        risk_note = 'The stock is trading meaningfully below its recent average, so caution is needed.'
    elif below_avg:
        risk_level = 'Medium'
        risk_note = 'The stock is below its recent average, which can signal recovery potential but also weakness.'
    else:
        risk_level = 'Low'
        risk_note = 'The stock is holding near or above its recent average, which is usually healthier.'

    if eligibility_score < 55:
        trade_type = 'Avoid'
        trade_reason = 'The stock does not show a strong enough setup for a new trade.'
    elif trading_style == 'Intraday':
        if 55 <= rsi <= 70 and macd_l > macd_s_val and pct_chg > 0.3:
            trade_type = 'Intraday'
            trade_reason = 'Momentum and RSI are supportive for a quick entry and exit.'
        elif ema_20 > ema_50:
            trade_type = 'Swing'
            trade_reason = 'The trend is positive, but this setup is better for a short swing.'
        else:
            trade_type = 'Avoid'
            trade_reason = 'The stock lacks a clean intraday pattern right now.'
    else:
        if ema_20 > ema_50 and 45 <= rsi <= 70 and pct_chg > 0.5:
            trade_type = 'Delivery'
            trade_reason = 'The trend is healthy and this stock looks suitable for positional/delivery buying.'
        elif ema_20 > ema_50:
            trade_type = 'Swing'
            trade_reason = 'The trend is positive and suits a swing or positional hold.'
        else:
            trade_type = 'Avoid'
            trade_reason = 'The stock does not show a strong longer-term setup.'

    confidence_label = 'High' if eligibility_score >= 70 else ('Medium' if eligibility_score >= 55 else 'Low')

    company_position = 'Strong' if (market_cap and market_cap > 1e10 and debt_to_equity is not None and debt_to_equity < 1.0) else ('Stable' if (market_cap and market_cap > 1e9) else 'Needs Review')

    return {
        'eligible_status': eligibility_status,
        'eligibility_note': eligibility_note,
        'eligibility_score': eligibility_score,
        'trade_type': trade_type,
        'trade_reason': trade_reason,
        'risk_level': risk_level,
        'risk_note': risk_note,
        'confidence_label': confidence_label,
        'below_avg': below_avg,
        'avg_gap_pct': avg_gap_pct,
        'company_position': company_position,
    }


def analyze_symbol_for_ui(symbol, total_capital, trading_style):
    try:
        sym = normalize_symbol(symbol)
        tkr = yf.Ticker(sym)
        hist = tkr.history(period='6mo', interval='1d')
        if hist.empty:
            hist = tkr.history(period='5d', interval='15m')
        if hist.empty:
            return None

        df = hist.copy()
        df.dropna(subset=['Close'], inplace=True)
        if df.empty or len(df) < 20:
            return None

        ltp = float(df['Close'].iloc[-1])
        qty = int(np.floor(total_capital / (ltp + 20)))
        O, H, L, C = df['Open'].values, df['High'].values, df['Low'].values, df['Close'].values
        body = abs(C[-1] - O[-1])
        lower_shadow = min(O[-1], C[-1]) - L[-1]
        upper_shadow = H[-1] - max(O[-1], C[-1])
        is_hammer = (body > 0) and (lower_shadow >= 2 * body) and (upper_shadow <= 0.2 * body)
        is_engulfing = len(C) > 1 and C[-1] > O[-1] and C[-2] < O[-2] and C[-1] >= O[-2] and O[-1] <= C[-2]
        c_shape = '🔨 Hammer' if is_hammer else ('🔥 Engulfing' if is_engulfing else '⏳ Consolidating')

        close = df['Close']
        high_s = df['High']
        low_s = df['Low']
        ema_20 = float(ta.trend.EMAIndicator(close=close, window=20).ema_indicator().iloc[-1])
        ema_50 = float(ta.trend.EMAIndicator(close=close, window=50).ema_indicator().iloc[-1])
        rsi = float(ta.momentum.RSIIndicator(close=close, window=14).rsi().iloc[-1])
        macd_o = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
        macd_l = float(macd_o.macd().iloc[-1])
        macd_s_val = float(macd_o.macd_signal().iloc[-1])
        atr_v = float(ta.volatility.AverageTrueRange(high=high_s, low=low_s, close=close, window=14).average_true_range().iloc[-1])

        # Enhanced accuracy indicators
        raw_vol = float(df['Volume'].iloc[-1])
        vol_avg_20 = float(df['Volume'].rolling(20).mean().iloc[-1]) if len(df) >= 20 else 0
        vol_spike_s = raw_vol > 1.5 * vol_avg_20 if vol_avg_20 > 0 else False
        try:
            adx_v = float(ta.trend.ADXIndicator(high=high_s, low=low_s, close=close, window=14).adx().iloc[-1])
        except Exception:
            adx_v = 0.0
        high_52w_s = float(df['High'].tail(252).max())
        low_52w_s = float(df['Low'].tail(252).min())
        price_pct_from_low = (ltp - low_52w_s) / (high_52w_s - low_52w_s + 1e-9)
        near_52w_low_s = price_pct_from_low < 0.15
        try:
            weekly_close_s = df['Close'].resample('W').last().dropna()
            if len(weekly_close_s) >= 21:
                w_ema8 = float(ta.trend.EMAIndicator(close=weekly_close_s, window=8).ema_indicator().iloc[-1])
                w_ema21 = float(ta.trend.EMAIndicator(close=weekly_close_s, window=21).ema_indicator().iloc[-1])
                weekly_bullish_s = w_ema8 > w_ema21
            else:
                weekly_bullish_s = False
        except Exception:
            weekly_bullish_s = False
        try:
            bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
            bb_upper = float(bb.bollinger_hband().iloc[-1])
            bb_breakout_s = ltp > bb_upper * 0.98
        except Exception:
            bb_breakout_s = False

        pct_chg = float(((C[-1] - C[-2]) / C[-2]) * 100) if len(C) > 1 else 0.0

        recommendation = build_stock_recommendation(sym, sym, df, total_capital, trading_style)
        acc = 40
        if ltp > ema_20: acc += 12
        if ema_20 > ema_50: acc += 12
        if trading_style == 'Intraday':
            if 50 <= rsi <= 70: acc += 18
            if macd_l > macd_s_val: acc += 15
            if pct_chg > 0.3: acc += 5
            if is_hammer or is_engulfing: acc += 8
        else:
            if 45 <= rsi <= 65: acc += 15
            if macd_l > macd_s_val: acc += 10
            if is_hammer or is_engulfing: acc += 10

        if adx_v > 20: acc += 8
        if vol_spike_s: acc += 10
        if not near_52w_low_s: acc += 5
        if weekly_bullish_s: acc += 12
        if bb_breakout_s: acc += 6

        if trading_style == 'Intraday':
            if acc >= 70: badge = 'BUY'
            elif acc >= 55: badge = 'HOLD'
            else: badge = 'AVOID'
        else:
            if acc >= 75: badge = 'BUY'
            elif acc >= 55: badge = 'HOLD'
            else: badge = 'AVOID'

        if trading_style == 'Intraday':
            if is_engulfing and rsi > 60: horizon = '⚡ Intraday Breakout (Same Day)'
            elif ltp > ema_20 and ema_20 > ema_50: horizon = '⏳ Short Momentum (1-2 Days)'
            else: horizon = '📈 Quick Range Play'
        else:
            if is_engulfing and rsi > 60: horizon = '⚡ Momentum Breakout (24-48 Hrs)'
            elif ltp > ema_20 and ema_20 > ema_50: horizon = '📅 Swing Trade (3-7 Days)'
            else: horizon = '⏳ Accumulation (2-4 Weeks)'

        target_p = round(ltp + 2 * (atr_v if (not pd.isna(atr_v) and atr_v > 0) else ltp * 0.03), 2)
        stoploss_p = round(ltp - 1 * (atr_v if (not pd.isna(atr_v) and atr_v > 0) else ltp * 0.03), 2)

        return {
            'name': sym,
            'sym': sym,
            'ltp': ltp,
            'qty': qty,
            'pct_chg': pct_chg,
            'rsi': rsi,
            'ema_20': ema_20,
            'ema_50': ema_50,
            'c_shape': c_shape,
            'acc': acc,
            'badge': badge,
            'horizon': horizon,
            'target': target_p,
            'stoploss': stoploss_p,
            'volume': raw_vol,
            'df': df,
            'macd_l': macd_l,
            'macd_s_val': macd_s_val,
            'mode': trading_style,
            'eligible_status': recommendation['eligible_status'],
            'eligibility_note': recommendation['eligibility_note'],
            'eligibility_score': recommendation['eligibility_score'],
            'trade_type': recommendation['trade_type'],
            'trade_reason': recommendation['trade_reason'],
            'risk_level': recommendation['risk_level'],
            'risk_note': recommendation['risk_note'],
            'confidence_label': recommendation['confidence_label'],
            'below_avg': recommendation['below_avg'],
            'avg_gap_pct': recommendation['avg_gap_pct'],
            'company_position': recommendation['company_position'],
        }
    except Exception:
        return None

# Free auto-refresh UI removed per user request.

# ===================================================================
# HEADER
# ===================================================================
# Free live refresh UI removed per user request.

c1, c2 = st.columns([0.07, 0.93])
with c1:
    st.markdown("<div style='font-size:40px; padding-top:6px;'>⚡</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<h1 style='margin:0; font-size:26px;'>i-7 Tech &nbsp;<span style='color:#6200EE;'>|</span>&nbsp; DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444; font-size:11px; margin:0; font-family:monospace;'>PRIVATE NSE ANALYTICS WORKSTATION · SNIPER ENGINE v2.0</p>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#1F2230; margin:10px 0 16px;'>", unsafe_allow_html=True)

# ===================================================================
# SIDEBAR
# ===================================================================
st.sidebar.markdown("## ⚙️ ENGINE CONFIG")
st.sidebar.markdown("<p style='color:#555; font-size:11px; font-family:monospace;'>TYPE YOUR CAPITAL AMOUNT ↓</p>", unsafe_allow_html=True)
# ---- Custom ticker input ----
custom_ticker = st.sidebar.text_input("Add custom ticker (e.g., RELIANCE.NS)", value="")
if st.sidebar.button("Add to Watchlist") and custom_ticker:
    if 'extra_tickers' not in st.session_state:
        st.session_state['extra_tickers'] = []
    if custom_ticker not in st.session_state['extra_tickers']:
        st.session_state['extra_tickers'].append(custom_ticker)
        st.sidebar.success(f"Added {custom_ticker} to watchlist")
single_stock_symbol = st.sidebar.text_input("Analyze one stock (e.g. RELIANCE.NS)", value="")
if st.sidebar.button("Analyze Stock") and single_stock_symbol:
    st.session_state['single_stock_analysis'] = normalize_symbol(single_stock_symbol)
    st.sidebar.success(f"Analyzing {normalize_symbol(single_stock_symbol)}")

# ---- AI Assistant toggle ----
show_ai_assistant = st.sidebar.checkbox("Enable AI Assistant", value=False, help="Show explanation why to buy the selected stock")
scan_universe = st.sidebar.radio(
    "Scan Universe",
    options=["Active Watchlist", "Nifty 500", "Full NSE (slow)"],
    index=2,
    help="Choose whether to scan only your watchlist, the Nifty 500, or the full NSE universe. Full NSE is much slower."
)
if scan_universe == "Full NSE (slow)":
    st.sidebar.markdown("<span style='color:#FFC107; font-size:11px;'>Warning: full NSE scan can take many minutes and may time out.</span>", unsafe_allow_html=True)
trading_style = st.sidebar.radio(
    "Trading Mode",
    options=["Swing", "Intraday"],
    index=0,
    help="Choose normal swing signals or intraday trading signals"
)
show_affordable_only = st.sidebar.checkbox("Show Affordable Only", value=True, help="Show only stocks where you can buy at least 1 share with your budget")

with st.sidebar.expander("💰 CAPITAL ALLOCATION"):
    total_capital = st.number_input(
        "Investment Capital (₹)",
        min_value=500,
        max_value=5000000,
        value=50000,
        step=500,
        help="Type your exact budget in Rupees — no dragging needed"
    )
    risk_tolerance = st.select_slider("Risk Appetite", options=["Conservative", "Moderate", "Aggressive"], value="Moderate")
    # ---- TARGET PRICE & TIME PREDICTION ----
    target_price = st.sidebar.number_input("Target Price (₹)", min_value=0.0, value=0.0, step=10.0)
    predict_days = st.sidebar.button("Predict Days to Target")

st.sidebar.markdown("<p style='color:#555; font-size:10px; font-family:monospace; text-transform:uppercase; letter-spacing:1px;'>Active Watchlist Nodes</p>", unsafe_allow_html=True)
for name in ACTIVE_WATCHLIST:
    st.sidebar.markdown(f"<span style='color:#00FF66; font-family:monospace; font-size:11px;'>▶ {name}</span>", unsafe_allow_html=True)

# ===================================================================
# SCAN BUTTON — Always visible, above tabs
# ===================================================================
scan_triggered = st.button("🔍  SCAN INDIAN MARKET NOW", use_container_width=True)

# ===================================================================
# SESSION STATE INIT
# ===================================================================
if 'scan_results' not in st.session_state:
    st.session_state['scan_results'] = []
if 'selected_stock' not in st.session_state:
    st.session_state['selected_stock'] = None
if 'single_stock_analysis' not in st.session_state:
    st.session_state['single_stock_analysis'] = None
if 'auto_scan_completed' not in st.session_state:
    st.session_state['auto_scan_completed'] = False

# ===================================================================
# SCAN ENGINE
# ===================================================================
run_scan = scan_triggered
if run_scan:
    results = []
    prog = st.progress(0)
    status_ph = st.empty()
    
    if trading_style == "Intraday" or scan_universe == "Active Watchlist":
        status_ph.markdown("<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Intraday/watchlist mode active: scanning watchlist tickers on 15-minute data ]</span>", unsafe_allow_html=True)
        tickers = list(ACTIVE_WATCHLIST.items())
        interval = "15m" if trading_style == "Intraday" else "1d"
        period = "5d" if trading_style == "Intraday" else "6mo"
    elif scan_universe == "Nifty 500":
        status_ph.markdown("<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Swing mode active: scanning Nifty 500 universe ]</span>", unsafe_allow_html=True)
        tickers = []
        try:
            df_list = pd.read_csv('https://archives.nseindia.com/content/indices/ind_nifty500list.csv')
            for symbol, name in zip(df_list['Symbol'], df_list['Company Name']):
                tickers.append((name, f"{symbol}.NS"))
        except Exception:
            tickers = list(ACTIVE_WATCHLIST.items())

        interval = "1d"
        period = "6mo"
    else:
        status_ph.markdown("<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Full NSE mode active: loading NSE symbol universe ]</span>", unsafe_allow_html=True)
        tickers = []
        try:
            df_list = pd.read_csv('https://archives.nseindia.com/content/equities/EQUITY_L.csv')
            for _, row in df_list.iterrows():
                symbol = str(row.get('SYMBOL', '')).strip()
                if not symbol or str(row.get('SERIES', '')).strip().upper() != 'EQ':
                    continue
                name = str(row.get('NAME OF COMPANY', row.get('SC_NAME', symbol))).strip()
                tickers.append((name or symbol, f"{symbol}.NS"))
            if not tickers:
                raise ValueError('No NSE equities found from EQUITY_L.csv')
        except Exception:
            try:
                status_ph.markdown("<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Falling back to Nifty 500 universe ]</span>", unsafe_allow_html=True)
                df_list = pd.read_csv('https://archives.nseindia.com/content/indices/ind_nifty500list.csv')
                for symbol, name in zip(df_list['Symbol'], df_list['Company Name']):
                    tickers.append((name, f"{symbol}.NS"))
                if not tickers:
                    raise ValueError('No Nifty 500 equities found')
            except Exception:
                tickers = list(ACTIVE_WATCHLIST.items())

        interval = "1d"
        period = "6mo"
    # Include any custom tickers added by the user
    if 'extra_tickers' in st.session_state:
        for ct in st.session_state['extra_tickers']:
            if ct not in [t[1] for t in tickers]:
                tickers.append((ct, ct))
    # Load bulk tickers from local csv if present
    csv_path = os.path.join(os.path.dirname(__file__), "tickers.csv")
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as f:
            bulk = [row[0].strip() for row in csv.reader(f) if row]
        for ct in bulk:
            if ct not in [t[1] for t in tickers]:
                tickers.append((ct, ct))
                
    # Run bulk download in smaller chunks to reduce hanging and errors
    interval_label = "15-minute" if trading_style == "Intraday" else "daily"
    status_ph.markdown(
        f"<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Downloading historical {interval_label} candles in batches for {len(tickers)} symbols. This may take several minutes. ]</span>",
        unsafe_allow_html=True
    )
    sym_list = [t[1] for t in tickers]
    data = pd.DataFrame()
    chunk_count = int(np.ceil(len(sym_list) / 100)) if sym_list else 0
    start_time = time.perf_counter()
    completed_batches = 0
    for chunk_idx, chunk in enumerate(chunk_list(sym_list, 100), start=1):
        try:
            batch_start = time.perf_counter()
            if chunk_count:
                progress_pct = min(100, int(chunk_idx / chunk_count * 100))
                prog.progress(progress_pct)
                elapsed_total = time.perf_counter() - start_time
                avg_batch_time = (elapsed_total / completed_batches) if completed_batches else (batch_start - start_time)
                remaining_batches = max(0, chunk_count - chunk_idx)
                eta_seconds = int(avg_batch_time * remaining_batches) if completed_batches else 0
                eta_label = format_eta(eta_seconds)
                status_ph.markdown(
                    f"<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Downloading batch {chunk_idx} of {chunk_count} — {len(chunk)} symbols ]<br>[ ETA: {eta_label} remaining • {progress_pct}% complete ]</span>",
                    unsafe_allow_html=True
                )
            else:
                status_ph.markdown(
                    f"<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Downloading batch {chunk_idx} of {chunk_count} — {len(chunk)} symbols ]</span>",
                    unsafe_allow_html=True
                )
            chunk_data = yf.download(chunk, period=period, interval=interval, group_by="ticker", threads=True, progress=False)
            if isinstance(chunk_data, pd.DataFrame) and not chunk_data.empty:
                data = pd.concat([data, chunk_data], axis=1)
            completed_batches += 1
        except Exception:
            continue
    prog.progress(100)
    if not data.empty:
        status_ph.markdown("<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Scanning complete. Pre-fetching company data in parallel... ]</span>", unsafe_allow_html=True)
        # Pre-warm the get_company_position cache in parallel so the per-stock loop is fast
        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(get_company_position, sym): sym for _, sym in tickers}
            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception:
                    pass
        status_ph.markdown("<span style='color:#00FF66; font-family:monospace; font-size:13px;'>[ Company data ready. Processing results... ]</span>", unsafe_allow_html=True)

    if data.empty:
        status_ph.markdown("<span style='color:#FF3366; font-family:monospace; font-size:13px;'>[ Error: no historical data could be downloaded ]</span>", unsafe_allow_html=True)
        st.session_state['scan_results'] = []
        st.session_state['selected_stock'] = None
        prog.empty()
        data = None

    if data is not None:
        for idx, (name, sym) in enumerate(tickers):
            try:
                # Support both multi-column (group_by='ticker') and single-frame returns
                if isinstance(data, pd.DataFrame) and data.columns.nlevels > 1 and 'Ticker' in data.columns.names:
                    if sym not in data.columns.get_level_values('Ticker'):
                        continue
                    df = data.xs(sym, level='Ticker', axis=1).copy()
                else:
                    # single-frame (e.g., when only one symbol requested)
                    if sym not in data.columns:
                        continue
                    df = data.copy()

                df.dropna(subset=['Close'], inplace=True)
                if df.empty or len(df) < 20:
                    continue

                ltp = float(df['Close'].iloc[-1])
                qty = int(np.floor(total_capital / (ltp + 20)))

                O, H, L, C = df['Open'].values, df['High'].values, df['Low'].values, df['Close'].values
                body = abs(C[-1] - O[-1])
                lower_shadow = min(O[-1], C[-1]) - L[-1]
                upper_shadow = H[-1] - max(O[-1], C[-1])
                is_hammer = (body > 0) and (lower_shadow >= 2 * body) and (upper_shadow <= 0.2 * body)
                is_engulfing = len(C) > 1 and C[-1] > O[-1] and C[-2] < O[-2] and C[-1] >= O[-2] and O[-1] <= C[-2]
                c_shape = "🔨 Hammer" if is_hammer else ("🔥 Engulfing" if is_engulfing else "⏳ Consolidating")

                close  = df['Close']
                high_s = df['High']
                low_s  = df['Low']

                ema_20 = float(ta.trend.EMAIndicator(close=close, window=20).ema_indicator().iloc[-1])
                ema_50 = float(ta.trend.EMAIndicator(close=close, window=50).ema_indicator().iloc[-1])
                rsi    = float(ta.momentum.RSIIndicator(close=close, window=14).rsi().iloc[-1])
                macd_o = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
                macd_l = float(macd_o.macd().iloc[-1])
                macd_s_val = float(macd_o.macd_signal().iloc[-1])
                atr_v  = float(ta.volatility.AverageTrueRange(high=high_s, low=low_s, close=close, window=14).average_true_range().iloc[-1])

                # Enhanced accuracy indicators
                vol_avg_20 = float(df['Volume'].rolling(20).mean().iloc[-1]) if len(df) >= 20 else 0
                vol_spike = float(df['Volume'].iloc[-1]) > 1.5 * vol_avg_20 if vol_avg_20 > 0 else False
                try:
                    adx_v = float(ta.trend.ADXIndicator(high=high_s, low=low_s, close=close, window=14).adx().iloc[-1])
                except Exception:
                    adx_v = 0.0
                high_52w_e = float(df['High'].tail(252).max())
                low_52w_e = float(df['Low'].tail(252).min())
                price_pct_from_low = (ltp - low_52w_e) / (high_52w_e - low_52w_e + 1e-9)
                near_52w_low = price_pct_from_low < 0.15
                try:
                    weekly_close_e = df['Close'].resample('W').last().dropna()
                    if len(weekly_close_e) >= 21:
                        w_ema8 = float(ta.trend.EMAIndicator(close=weekly_close_e, window=8).ema_indicator().iloc[-1])
                        w_ema21 = float(ta.trend.EMAIndicator(close=weekly_close_e, window=21).ema_indicator().iloc[-1])
                        weekly_bullish = w_ema8 > w_ema21
                    else:
                        weekly_bullish = False
                except Exception:
                    weekly_bullish = False
                try:
                    bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
                    bb_upper = float(bb.bollinger_hband().iloc[-1])
                    bb_breakout = ltp > bb_upper * 0.98
                except Exception:
                    bb_breakout = False

                news_score = None
                pct_chg = float(((C[-1] - C[-2]) / C[-2]) * 100) if len(C) > 1 else 0.0

                acc = 40
                if ltp > ema_20: acc += 12
                if ema_20 > ema_50: acc += 12
                if trading_style == "Intraday":
                    if 50 <= rsi <= 70: acc += 18
                    if macd_l > macd_s_val: acc += 15
                    if pct_chg > 0.3: acc += 5
                    if is_hammer or is_engulfing: acc += 8
                else:
                    if 45 <= rsi <= 65: acc += 15
                    if macd_l > macd_s_val: acc += 10
                    if is_hammer or is_engulfing: acc += 10

                if adx_v > 20: acc += 8
                if vol_spike: acc += 10
                if not near_52w_low: acc += 5
                if weekly_bullish: acc += 12
                if bb_breakout: acc += 6

                if trading_style == "Intraday":
                    if acc >= 70: badge = "BUY"
                    elif acc >= 55: badge = "HOLD"
                    else: badge = "AVOID"
                else:
                    if acc >= 75: badge = "BUY"
                    elif acc >= 55: badge = "HOLD"
                    else: badge = "AVOID"

                if trading_style == "Intraday":
                    if is_engulfing and rsi > 60: horizon = "⚡ Intraday Breakout (Same Day)"
                    elif ltp > ema_20 and ema_20 > ema_50: horizon = "⏳ Short Momentum (1-2 Days)"
                    else: horizon = "📈 Quick Range Play"
                else:
                    if is_engulfing and rsi > 60: horizon = "⚡ Momentum Breakout (24-48 Hrs)"
                    elif ltp > ema_20 and ema_20 > ema_50: horizon = "📅 Swing Trade (3-7 Days)"
                    else: horizon = "⏳ Accumulation (2-4 Weeks)"

                atr_safe = atr_v if (not pd.isna(atr_v) and atr_v > 0) else ltp * 0.03
                target_p    = round(ltp + 2 * atr_safe, 2)
                stoploss_p  = round(ltp - 1 * atr_safe, 2)
                raw_vol     = float(df['Volume'].iloc[-1])

                recommendation = build_stock_recommendation(name, sym, df, total_capital, trading_style)
                results.append({
                    'name': name, 'sym': sym, 'ltp': ltp, 'qty': qty,
                    'pct_chg': pct_chg, 'rsi': rsi, 'ema_20': ema_20, 'ema_50': ema_50,
                    'news_score': news_score, 'c_shape': c_shape,
                    'acc': acc, 'badge': badge, 'horizon': horizon,
                    'target': target_p, 'stoploss': stoploss_p,
                    'volume': raw_vol, 'df': df,
                    'macd_l': macd_l, 'macd_s_val': macd_s_val,
                    'mode': trading_style,
                    'eligible_status': recommendation['eligible_status'],
                    'eligibility_note': recommendation['eligibility_note'],
                    'eligibility_score': recommendation['eligibility_score'],
                    'trade_type': recommendation['trade_type'],
                    'trade_reason': recommendation['trade_reason'],
                    'risk_level': recommendation.get('risk_level', 'Unknown'),
                    'risk_note': recommendation.get('risk_note', ''),
                    'confidence_label': recommendation.get('confidence_label', 'Low'),
                    'below_avg': recommendation.get('below_avg', False),
                    'avg_gap_pct': recommendation.get('avg_gap_pct', 0.0),
                    'company_position': recommendation.get('company_position', 'Unknown'),
                })
            except Exception:
                # Skip problematic symbols silently
                continue

    prog.empty()
    status_ph.empty()
    results.sort(key=lambda x: x['acc'], reverse=True)
    st.session_state['scan_results'] = results
    st.session_state['auto_scan_completed'] = True
    if results:
        st.session_state['selected_stock'] = results[0]['name']

# ===================================================================
# SINGLE STOCK ANALYZER
# ===================================================================
single_symbol = st.session_state.get('single_stock_analysis')
if single_symbol:
    with st.expander("📌 Single Stock Suitability", expanded=True):
        single_result = analyze_symbol_for_ui(single_symbol, total_capital, trading_style)
        if single_result is None:
            st.markdown(f"<div style='color:#FF3366;'>Could not fetch a valid chart for {single_symbol}.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:18px; font-weight:bold; color:#FFF; font-family:monospace; margin-bottom:8px;'>{single_result['name']} · {single_result['trade_type']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background:#1A1D24; border:1px solid #2A2D37; border-radius:10px; padding:12px; margin-bottom:10px;'>"
                        f"<div style='color:#00FF66; font-weight:bold;'>{single_result['eligible_status']}</div>"
                        f"<div style='color:#AAA; font-size:13px; margin-top:4px;'>{single_result['eligibility_note']}</div>"
                        f"<div style='margin-top:8px; color:#FFFFFF;'>Recommended trade: <b>{single_result['trade_type']}</b></div>"
                        f"<div style='color:#BBBBBB; font-size:13px; margin-top:4px;'>{single_result['trade_reason']}</div>"
                        f"</div>", unsafe_allow_html=True)
            st.metric("Current Price", f"₹{single_result['ltp']:,.2f}")
            st.metric("Suggested Trade", single_result['trade_type'])
            st.metric("Confidence", f"{single_result['acc']}%")

# ===================================================================
# TABS  — display only, no scan logic inside
# ===================================================================
tab_signals, tab_portfolio, tab_news, tab_rising = st.tabs(["📡  Signals", "💼  Portfolio", "📰  News", "📈  Rising"])

results = st.session_state.get('scan_results', [])

# ---- SIGNALS TAB ----
with tab_signals:
    if not results:
        st.markdown(
            "<div style='text-align:center; padding:80px 0; color:#333; font-family:monospace;'>"
            "[ SYSTEM STANDBY ]<br><br>"
            "<span style='color:#444;'>Set your capital in the sidebar, then press "
            "<span style='color:#00FF66;'>SCAN INDIAN MARKET NOW</span> above.</span>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        left_col, right_col = st.columns([1, 1.8], gap="large")

        # Left: Signal List
        with left_col:
            st.markdown("<div style='font-size:16px; font-weight:bold; color:#FFF; font-family:monospace; margin-bottom:10px;'>📡 Live Predictions</div>", unsafe_allow_html=True)
            
            # Badge filter
            badge_filter = st.radio("Signal Filter", options=["All", "BUY", "HOLD", "AVOID"], horizontal=True, label_visibility="collapsed")
            
            # Search input
            search_query = st.text_input("🔍 Search Stock Name/Symbol", value="").strip().lower()
            
            # Apply Filters
            filtered_results = results
            if show_affordable_only:
                filtered_results = [r for r in filtered_results if r['qty'] > 0]
            if badge_filter != "All":
                filtered_results = [r for r in filtered_results if r['badge'] == badge_filter]
            if search_query:
                filtered_results = [r for r in filtered_results if search_query in r['name'].lower() or search_query in r['sym'].lower()]
            
            if not filtered_results:
                st.markdown("<p style='color:#555; font-family:monospace;'>No stocks match current filter.</p>", unsafe_allow_html=True)
                stock_names = []
            else:
                slice_count = 50
                if len(filtered_results) > slice_count:
                    st.markdown(f"<p style='color:#888; font-size:11px; font-family:monospace;'>Showing top {slice_count} of {len(filtered_results)} stocks</p>", unsafe_allow_html=True)

                display_results = filtered_results[:slice_count]
                stock_names = [r['name'] for r in display_results]
                selected = st.session_state.get('selected_stock', stock_names[0])
                if selected not in stock_names:
                    selected = stock_names[0]

                # Top suggestion card
                top_stock = display_results[0]
                st.markdown(f"""
                <div style='background:#1F2230; padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid #6200EE;'>
                    <div style='color:#AAA; font-size:10px;'>🏆 TOP SUGGESTION (Highest Accuracy Within Budget)</div>
                    <div style='font-weight:bold; color:#FFF; font-size:14px;'>{top_stock['name']}</div>
                    <div style='color:#00FF66; font-size:12px;'>Confidence: {top_stock['acc']}% &nbsp;|&nbsp; {top_stock['badge']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"⚡ Inspect {top_stock['name']}"):
                    st.session_state['selected_stock'] = top_stock['name']
                    st.rerun()

                # Build radio labels: ⬡ Name   ±X.XX%   badge
                def _make_lbl(r):
                    pct = r['pct_chg']
                    pct_str = f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"
                    badge_sym = "🟢 BUY" if r['badge'] == "BUY" else ("🟡 HOLD" if r['badge'] == "HOLD" else "🔴 AVOID")
                    intraday_badge = " ⚡ INTRADAY" if r.get('mode') == "Intraday" else ""
                    return f"⬡ {r['name']}   {pct_str}   {badge_sym}{intraday_badge}"

                radio_labels   = [_make_lbl(r) for r in display_results]
                lbl_to_name    = {_make_lbl(r): r['name'] for r in display_results}
                cur_lbl        = next((_make_lbl(r) for r in display_results if r['name'] == selected), radio_labels[0])

                chosen_lbl = st.radio(
                    "Stocks",
                    options=radio_labels,
                    index=radio_labels.index(cur_lbl),
                    label_visibility="collapsed"
                )
                st.session_state['selected_stock'] = lbl_to_name[chosen_lbl]

        # Right: Detail Panel
        with right_col:
            sel = next((r for r in results if r['name'] == st.session_state['selected_stock']), results[0])
            
            # Dynamically fetch news_score for selected stock (lazy loading)
            if sel['news_score'] is None:
                with st.spinner("Retrieving news sentiment..."):
                    sel['news_score'] = fetch_sentiment(sel['sym'])
                    # Update accuracy points based on sentiment
                    if sel['news_score'] > 0.2:
                        sel['acc'] = min(100, sel['acc'] + 10)
                    elif sel['news_score'] <= -0.4:
                        sel['acc'] = 30
                    # Recompute badge
                    if sel['acc'] >= 75:
                        sel['badge'] = "BUY"
                    elif sel['acc'] >= 55:
                        sel['badge'] = "HOLD"
                    else:
                        sel['badge'] = "AVOID"
            
            df_sel = sel['df']
            pct = sel['pct_chg']
            pct_color = "#00FF66" if pct >= 0 else "#FF3366"
            pct_str = f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"
            acc_pct = sel['acc']
            gauge_deg = int((acc_pct / 100) * 360)
            sentiment_color = "#00FF66" if acc_pct >= 70 else ("#FFC107" if acc_pct >= 50 else "#FF3366")
            sentiment_label = "Bullish" if acc_pct >= 70 else ("Neutral" if acc_pct >= 50 else "Bearish")
            # --- BUY/SELL ALERT OPTION ---
            show_alert = st.sidebar.checkbox("Show Buy/Sell Alerts", value=True, help="Toggle visual alerts for buy or sell signals")

            g_col, p_col = st.columns([1, 1.5])
            with g_col:
                st.markdown(f"""
                <div class='gauge-card'>
                    <div class='gauge-ring' style='--pct: {gauge_deg}deg;'>
                        <div class='gauge-inner'>
                            <div class='gauge-val'>{acc_pct}%</div>
                            <div class='gauge-sub'>SIGNAL<br>CONFIDENCE</div>
                        </div>
                    </div>
                    <div style='color:#888; font-size:10px; font-family:monospace; margin-top:4px;'>ACCURACY SCORE</div>
                </div>
                """, unsafe_allow_html=True)

            with p_col:
                live_quote = get_live_quote(sel['sym'])
                live_price = live_quote['price']
                price_text = f"₹{live_price:,.2f}" if live_price is not None else f"₹{sel['ltp']:,.2f}"
                st.markdown(f"""
                <div style='padding: 20px 0 0 10px;'>
                    <div style='font-size:40px; font-weight:bold; color:{pct_color}; font-family:monospace; line-height:1;'>{pct_str}</div>
                    <div style='font-size:22px; font-weight:bold; color:#FFF; font-family:monospace; margin-top:4px;'>{sel["name"]}</div>
                    <div style='margin-top:8px; background:#12151E; border:1px solid #2A2D37; border-radius:10px; padding:10px 12px; display:inline-block;'>
                        <div style='color:#888; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Live Quote</div>
                        <div style='color:#FFFFFF; font-size:20px; font-weight:bold; font-family:monospace;'>{price_text}</div>
                        <div style='color:#00FF66; font-size:12px; font-family:monospace;'>Updated from free Yahoo Finance feed</div>
                    </div>
                    <div style='font-size:18px; color:#AAA; font-family:monospace; margin-top:2px;'>
                        ₹{sel["ltp"]:,.2f} &nbsp;<span style='color:{pct_color};'>{"▲" if pct >= 0 else "▼"}</span>
                    </div>
                    <div style='margin-top:10px;'>
                        <span style='background:#1A1D24; border:1px solid #333; color:#AAA; font-size:11px; padding:3px 8px; border-radius:4px; font-family:monospace;'>{sel["c_shape"]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='color:#888; font-size:12px; font-family:monospace; margin:14px 0 2px;'>📈 Candlestick (30‑Day) Performance</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:#1A1D24; border:1px solid #2A2D37; border-radius:10px; padding:12px; margin-bottom:12px;'>
                <div style='font-size:14px; font-weight:bold; color:#FFFFFF; margin-bottom:6px;'>🎯 Stock Suitability</div>
                <div style='color:#00FF66; font-weight:bold;'>{sel['eligible_status']}</div>
                <div style='color:#AAA; font-size:13px; margin-top:4px;'>{sel['eligibility_note']}</div>
                <div style='margin-top:8px; color:#FFFFFF;'>Recommended trade: <b>{sel['trade_type']}</b></div>
                <div style='color:#BBBBBB; font-size:13px; margin-top:4px;'>{sel['trade_reason']}</div>
                <div style='margin-top:8px; color:#FFC107;'>Risk: <b>{sel['risk_level']}</b></div>
                <div style='color:#BBBBBB; font-size:13px; margin-top:4px;'>{sel['risk_note']}</div>
                <div style='margin-top:8px; color:#00FF66;'>Confidence: <b>{sel['confidence_label']}</b></div>
                <div style='color:#BBBBBB; font-size:13px; margin-top:4px;'>Company position: <b>{sel['company_position']}</b></div>
                <div style='color:#BBBBBB; font-size:13px; margin-top:4px;'>Current price is {sel['avg_gap_pct']:+.2f}% vs 50-day average.</div>
            </div>
            """, unsafe_allow_html=True)
            import plotly.graph_objects as go
            candles = go.Figure(data=[go.Candlestick(x=df_sel.index[-30:],
                            open=df_sel['Open'][-30:],
                            high=df_sel['High'][-30:],
                            low=df_sel['Low'][-30:],
                            close=df_sel['Close'][-30:])])
            candles.update_layout(margin=dict(l=0,r=0,b=0,t=0), height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(candles, use_container_width=True)

            # 4 metric mini-cards
            m1, m2, m3, m4 = st.columns(4)
            vol_str = f"₹{sel['volume']/1e7:.1f}Cr" if sel['volume'] > 1e7 else f"{sel['volume']/1e6:.1f}M"
            rsi_lbl = "Overbought" if sel['rsi'] > 70 else ("Oversold" if sel['rsi'] < 30 else "Neutral")
            with m1: st.markdown(f"<div class='mini-card'><div class='label'>24h Volume</div><div class='value'>{vol_str}</div></div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='mini-card'><div class='label'>RSI (14)</div><div class='value'>{sel['rsi']:.1f}</div><div style='font-size:10px;color:#888;'>({rsi_lbl})</div></div>", unsafe_allow_html=True)
            with m3: st.markdown(f"<div class='mini-card'><div class='label'>Sentiment</div><div class='value' style='color:{sentiment_color};'>{sentiment_label}</div></div>", unsafe_allow_html=True)
            with m4: st.markdown(f"<div class='mini-card'><div class='label'>Affordable Qty</div><div class='value'>{sel['qty']}</div></div>", unsafe_allow_html=True)

            # Risk boundaries
            st.markdown("<div style='font-size:15px; font-weight:bold; color:#FFF; font-family:monospace; margin:14px 0 6px;'>🛡️ Risk Boundaries</div>", unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1: st.markdown(f"<div class='mini-card'><div class='label'>Current Price</div><div class='value'>₹{sel['ltp']:,.2f}</div></div>", unsafe_allow_html=True)
            with r2: st.markdown(f"<div class='mini-card'><div class='label'>🎯 Target</div><div class='value' style='color:#00FF66;'>₹{sel['target']:,.2f}</div></div>", unsafe_allow_html=True)
            with r3: st.markdown(f"<div class='mini-card'><div class='label'>🛑 Stop-Loss</div><div class='value' style='color:#FF3366;'>₹{sel['stoploss']:,.2f}</div></div>", unsafe_allow_html=True)

            # ---- AI Assistant explanation ----
            if show_ai_assistant:
                # Ensure news_score is a float for formatting
                news_score_val = sel['news_score'] if sel['news_score'] is not None else 0.0
                explanation = f"**Why consider buying {sel['name']}?**\n"
                explanation += f"- Current price: ₹{sel['ltp']:,.2f} (change {pct_str})\n"
                explanation += f"- EMA20 ({sel['ema_20']:.2f}) {'above' if sel['ltp'] > sel['ema_20'] else 'below'} EMA20\n"
                explanation += f"- EMA50 ({sel['ema_50']:.2f}) {'above' if sel['ema_20'] > sel['ema_50'] else 'below'} EMA50\n"
                explanation += f"- RSI: {sel['rsi']:.1f} ({'neutral' if 45 <= sel['rsi'] <= 65 else ('overbought' if sel['rsi'] > 65 else 'oversold')})\n"
                explanation += f"- MACD line {'above' if sel['macd_l'] > sel['macd_s_val'] else 'below'} signal\n"
                explanation += f"- Candlestick pattern: {sel['c_shape']}\n"
                explanation += f"- News sentiment score: {news_score_val:.2f}\n"
                explanation += f"- Accuracy confidence: {sel['acc']}% (badge: {sel['badge']})\n"
                st.markdown(f"<div style='background:#1A1D24; padding:12px; border-radius:8px; margin-top:12px; color:#E0E0E0;'>{explanation}</div>", unsafe_allow_html=True)
                # Time-to-target prediction display
                if predict_days and target_price > 0:
                    # Simple estimate based on average daily change over last 30 days
                    recent = df_sel['Close'].tail(30)
                    if len(recent) > 1:
                        daily_change = recent.diff().mean()
                        if daily_change > 0:
                            days_needed = max(0, int((target_price - sel['ltp']) / daily_change))
                            st.markdown(f"<div style='margin-top:12px; color:#00FF66;'>⏳ Estimated {days_needed} trading days to reach ₹{target_price:,.2f}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='margin-top:12px; color:#FF3366;'>📉 Target price unlikely to be reached (negative trend).</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='margin-top:12px; color:#FF3366;'>⚠️ Not enough data for prediction.</div>", unsafe_allow_html=True)

# ---- PORTFOLIO TAB ----
with tab_portfolio:
    st.markdown(
        "<div style='text-align:center; padding:80px 0; color:#333; font-family:monospace;'>"
        "[ PORTFOLIO MODULE ]<br><br>"
        "<span style='color:#444;'>Scan the market first. Your affordable positions will appear here.</span>"
        "</div>",
        unsafe_allow_html=True
    )

# ---- NEWS TAB ----
with tab_news:
    st.markdown(
        "<div style='text-align:center; padding:80px 0; color:#333; font-family:monospace;'>"
        "[ NEWS FEED MODULE ]<br><br>"
        "<span style='color:#444;'>News sentiment is analyzed per stock during each scan.</span>"
        "</div>",
        unsafe_allow_html=True
    )

# ---- RISING TAB ----
with tab_rising:
    if not results:
        st.markdown(
            "<div style='text-align:center; padding:80px 0; color:#333; font-family:monospace;'>"
            "[ SYSTEM STANDBY ]<br><br>"
            "<span style='color:#444;'>Run a market scan first to discover recovery candidates.</span>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        # ── Info banner ──────────────────────────────────────
        st.markdown(
            "<div style='background:#1A1D24; border:1px solid #FFC107; border-radius:10px; padding:12px 16px; margin-bottom:16px;'>"
            "<div style='color:#FFC107; font-weight:bold; font-family:monospace; font-size:14px;'>🚀 RISING — DIP RECOVERY SCANNER</div>"
            "<div style='color:#888; font-size:12px; margin-top:4px;'>"
            "Stocks that fell <b>10%+ in the last month</b> but are now showing early reversal signals: "
            "RSI entering recovery zone + MACD reversal or bullish candle (Hammer / Engulfing)."
            "</div></div>",
            unsafe_allow_html=True
        )

        # ── Build candidate list ──────────────────────────────
        rising_candidates = []
        for r in results:
            try:
                df_r = r.get('df')
                if df_r is None or len(df_r) < 22:
                    continue
                close_21d_ago = float(df_r['Close'].iloc[-22])
                close_now = r['ltp']
                monthly_pct = ((close_now - close_21d_ago) / close_21d_ago) * 100

                is_big_fall      = monthly_pct < -10
                in_recovery_rsi  = 20 <= r['rsi'] <= 55
                reversal_signal  = (
                    r['macd_l'] > r['macd_s_val'] or
                    r['c_shape'] in ['🔨 Hammer', '🔥 Engulfing']
                )

                if is_big_fall and in_recovery_rsi and reversal_signal:
                    rising_candidates.append({**r, 'monthly_pct': monthly_pct})
            except Exception:
                continue

        # Sort: biggest fall first (most recovery potential)
        rising_candidates.sort(key=lambda x: x['monthly_pct'])

        if not rising_candidates:
            st.markdown(
                "<div style='text-align:center; padding:40px 0; color:#555; font-family:monospace;'>"
                "[ No dip recovery candidates in current scan ]<br>"
                "<span style='color:#444;'>Try scanning Nifty 500 or Full NSE for more candidates.</span>"
                "</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='color:#00FF66; font-family:monospace; font-size:12px; margin-bottom:12px;'>"
                f"📊 {len(rising_candidates)} recovery candidate(s) found</div>",
                unsafe_allow_html=True
            )
            for rc in rising_candidates[:20]:
                rsi_color    = '#FF3366' if rc['rsi'] < 30 else ('#FFC107' if rc['rsi'] < 45 else '#00FF66')
                signal_text  = rc['c_shape'] if rc['c_shape'] != '⏳ Consolidating' else ''
                if rc['macd_l'] > rc['macd_s_val']:
                    signal_text = (signal_text + '  📊 MACD↑').strip()
                fall_pct_str = f"{rc['monthly_pct']:.1f}%"
                st.markdown(f"""
                <div style='background:#12151E; border:1px solid #2A2D37;
                     border-left:4px solid #FFC107; border-radius:10px;
                     padding:14px 16px; margin-bottom:12px;'>
                    <div style='display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;'>
                        <div>
                            <div style='font-weight:bold; color:#FFFFFF; font-size:15px;
                                 font-family:monospace;'>{rc['name']}</div>
                            <div style='color:#888; font-size:11px;'>{rc['sym']}</div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='color:#FF3366; font-size:20px; font-weight:bold;
                                 font-family:monospace;'>{fall_pct_str}</div>
                            <div style='color:#888; font-size:10px;'>30-day fall</div>
                        </div>
                    </div>
                    <div style='margin-top:12px; display:flex; gap:24px; flex-wrap:wrap;'>
                        <div><div style='color:#888; font-size:10px; text-transform:uppercase;'>RSI</div>
                             <div style='color:{rsi_color}; font-weight:bold; font-size:15px;'>{rc['rsi']:.1f}</div></div>
                        <div><div style='color:#888; font-size:10px; text-transform:uppercase;'>Price</div>
                             <div style='color:#FFF; font-weight:bold; font-size:15px;'>₹{rc['ltp']:,.2f}</div></div>
                        <div><div style='color:#888; font-size:10px; text-transform:uppercase;'>🎯 Target</div>
                             <div style='color:#00FF66; font-weight:bold; font-size:15px;'>₹{rc['target']:,.2f}</div></div>
                        <div><div style='color:#888; font-size:10px; text-transform:uppercase;'>🛑 Stop-Loss</div>
                             <div style='color:#FF3366; font-weight:bold; font-size:15px;'>₹{rc['stoploss']:,.2f}</div></div>
                        <div><div style='color:#888; font-size:10px; text-transform:uppercase;'>Signal</div>
                             <div style='color:#FFC107; font-weight:bold; font-size:13px;'>{signal_text or '—'}</div></div>
                        <div><div style='color:#888; font-size:10px; text-transform:uppercase;'>Affordable Qty</div>
                             <div style='color:#FFF; font-weight:bold; font-size:15px;'>{rc['qty']}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ===================================================================
# FOOTER
# ===================================================================
st.markdown("""
<div class="footer-cta">
    🤖 <b>SUGGESTION ENGINE ACTIVE</b><br>
    Open <b>Groww</b> → Search <b>[Stock Symbol]</b> → Order <b>[Affordable Qty]</b> shares → Set <b>Target</b> & <b>Stop-Loss</b> as shown.
</div>
""", unsafe_allow_html=True)
