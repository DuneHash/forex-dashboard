# app_multi_pairs.py

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

st.set_page_config(layout="wide")
st.title("📊 Forex Pairs Comparison Dashboard")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Settings")

# Πολλαπλά Forex pairs
all_pairs = [
    "NZDUSD=X", "AUDUSD=X", "EURUSD=X", "GBPUSD=X", "EURAUD=X", "EURNZD=X", "EURJPY=X", "GBPJPY=X"
]

selected_pairs = st.sidebar.multiselect(
    "Select Forex Pairs",
    all_pairs,
    default=["NZDUSD=X", "AUDUSD=X"]
)

timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=2
)

rolling_window = st.sidebar.slider("Rolling Correlation Window", 5, 100, 30)

show_candles = st.sidebar.checkbox("Show Candlestick Charts", True)

# Optional toggle για Live TV
show_tv = st.sidebar.checkbox("Show Live TV", value=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(symbols, period):
    data = yf.download(symbols, period=period)
    return data

data = load_data(selected_pairs, timeframe)
close = data["Close"].dropna()

# =========================
# NORMALIZED CHART
# =========================
st.subheader("📈 Normalized Comparison")

normalized = close / close.iloc[0] * 100

fig1, ax1 = plt.subplots(figsize=(12,6))
for pair in selected_pairs:
    ax1.plot(normalized[pair], label=pair)

ax1.legend()
ax1.grid()
st.pyplot(fig1)

# =========================
# CORRELATION MATRIX
# =========================
st.subheader("🔗 Correlation Matrix")

corr_matrix = close.corr()
st.dataframe(corr_matrix.style.format("{:.2f}"))

# =========================
# ROLLING CORRELATION
# =========================
st.subheader("📊 Rolling Correlation (First 2 Selected Pairs)")

if len(selected_pairs) >= 2:
    rolling_corr = close[selected_pairs[0]].rolling(rolling_window).corr(close[selected_pairs[1]])

    fig2, ax2 = plt.subplots(figsize=(12,4))
    ax2.plot(rolling_corr)
    ax2.axhline(0, linestyle="--")
    ax2.set_title(f"{rolling_window}-Day Rolling Correlation: {selected_pairs[0]} vs {selected_pairs[1]}")
    ax2.grid()
    st.pyplot(fig2)
else:
    st.info("Select at least 2 pairs for rolling correlation.")

# =========================
# SPREAD
# =========================
st.subheader("📉 Spread (First 2 Selected Pairs)")

if len(selected_pairs) >= 2:
    spread = close[selected_pairs[1]] - close[selected_pairs[0]]

    fig3, ax3 = plt.subplots(figsize=(12,4))
    ax3.plot(spread)
    ax3.set_title(f"Spread: {selected_pairs[1]} - {selected_pairs[0]}")
    ax3.grid()
    st.pyplot(fig3)

# =========================
# CANDLESTICKS
# =========================
if show_candles:
    st.subheader("🕯️ Candlestick Charts")

    cols = st.columns(len(selected_pairs))
    for i, pair in enumerate(selected_pairs):
        df = data.xs(pair, axis=1, level=1).dropna()
        fig, ax = plt.subplots()
        mpf.plot(
            df,
            type="candle",
            style="charles",
            ax=ax,
            volume=False
        )
        cols[i].pyplot(fig)

# =========================
# LIVE TV (Bloomberg)
# =========================
if show_tv:
    st.subheader("📺 Live Market TV")

    st.markdown(
        """
        **Source:** Bloomberg (via YouTube)  
        ⚠️ This content is embedded from an official YouTube stream and is not owned or hosted by this dashboard.
        """
    )

    # Βάλε εδώ το URL του YouTube live stream
    bloomberg_url = "https://www.youtube.com/watch?v=iEpJwprxDdk"

    st.video(bloomberg_url)
    st.divider()
    st.caption("Live financial news stream for informational purposes only.")