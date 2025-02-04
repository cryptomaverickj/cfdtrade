import streamlit as st
import MetaTrader5 as mt5
import time

# Initialize connection to MT5
if not mt5.initialize():
    st.error("Failed to connect to MT5")
    st.stop()

SYMBOL = "EURUSD"  # Trading pair

# Initialize session state variables
if 'balance' not in st.session_state:
    st.session_state.balance = 10000.0  # Starting balance
if 'position' not in st.session_state:
    st.session_state.position = None  # No position initially
if 'entry_price' not in st.session_state:
    st.session_state.entry_price = 0.0  # Entry price of the position
if 'current_price' not in st.session_state:
    st.session_state.current_price = 0.0  # Will be updated with live data

# Function to fetch live price from MT5
def fetch_live_price():
    tick = mt5.symbol_info_tick(SYMBOL)
    if tick:
        st.session_state.current_price = tick.ask  # Using Ask price for buy trades

# Function to open a long position
def buy():
    if st.session_state.position is not None:
        st.error("You already have an open position.")
        return
    st.session_state.position = "Long"
    st.session_state.entry_price = st.session_state.current_price
    st.success(f"Opened Long Position at ${st.session_state.entry_price:.5f}")

# Function to open a short position
def sell():
    if st.session_state.position is not None:
        st.error("You already have an open position.")
        return
    st.session_state.position = "Short"
    st.session_state.entry_price = st.session_state.current_price
    st.success(f"Opened Short Position at ${st.session_state.entry_price:.5f}")

# Function to close the current position
def close_position():
    if st.session_state.position is None:
        st.error("No open position to close.")
        return
    
    # Calculate profit/loss
    profit = 0
    if st.session_state.position == "Long":
        profit = (st.session_state.current_price - st.session_state.entry_price) * 100000  # Standard lot size
    elif st.session_state.position == "Short":
        profit = (st.session_state.entry_price - st.session_state.current_price) * 100000
    
    # Update balance
    st.session_state.balance += profit
    st.session_state.position = None
    st.success(f"Position closed. Profit: ${profit:.2f}")

# Streamlit app layout
st.title("Live CFD/Forex Trading Simulator with MT5")

# Fetch and display live price
time.sleep(1)  # Avoid frequent API calls
fetch_live_price()
st.write(f"**Balance:** ${st.session_state.balance:.2f}")
st.write(f"**Current Price (EUR/USD):** ${st.session_state.current_price:.5f}")

# Buttons for trading actions
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Buy"):
        buy()
with col2:
    if st.button("Sell"):
        sell()
with col3:
    if st.button("Close Position"):
        close_position()

# Shutdown MT5 connection
mt5.shutdown()
