import streamlit as st
import random
import time

# Initialize session state variables
if 'balance' not in st.session_state:
    st.session_state.balance = 10000.0  # Starting balance
if 'position' not in st.session_state:
    st.session_state.position = None  # No position initially
if 'entry_price' not in st.session_state:
    st.session_state.entry_price = 0.0  # Entry price of the position
if 'current_price' not in st.session_state:
    st.session_state.current_price = 100.0  # Simulated current price

# Function to update the current price
def update_price():
    st.session_state.current_price += random.uniform(-1.0, 1.0)  # Simulate price movement

# Function to open a long position
def buy():
    if st.session_state.position is not None:
        st.error("You already have an open position.")
        return
    st.session_state.position = "Long"
    st.session_state.entry_price = st.session_state.current_price
    st.success(f"Opened Long Position at ${st.session_state.entry_price:.2f}")

# Function to open a short position
def sell():
    if st.session_state.position is not None:
        st.error("You already have an open position.")
        return
    st.session_state.position = "Short"
    st.session_state.entry_price = st.session_state.current_price
    st.success(f"Opened Short Position at ${st.session_state.entry_price:.2f}")

# Function to close the current position
def close_position():
    if st.session_state.position is None:
        st.error("No open position to close.")
        return
    
    # Calculate profit/loss
    profit = 0
    if st.session_state.position == "Long":
        profit = st.session_state.current_price - st.session_state.entry_price
    elif st.session_state.position == "Short":
        profit = st.session_state.entry_price - st.session_state.current_price
    
    # Update balance
    st.session_state.balance += profit
    st.session_state.position = None
    st.success(f"Position closed. Profit: ${profit:.2f}")

# Streamlit app layout
st.title("CFD/Forex Trading Simulator")

# Display balance and current price
st.write(f"**Balance:** ${st.session_state.balance:.2f}")
st.write(f"**Current Price:** ${st.session_state.current_price:.2f}")

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

# Simulate price updates
while True:
    time.sleep(1)  # Wait 1 second between price updates
    update_price()
    st.experimental_rerun()  # Refresh the app to display updated price
