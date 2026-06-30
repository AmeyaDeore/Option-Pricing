import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata
import os

st.set_page_config(layout="wide", page_title="3D Options Analytics Surface")

from ui_components import apply_custom_sidebar
apply_custom_sidebar()

st.title("3D Options Analytics Surface")
st.markdown("This application fetches real-time options data, calculates implied volatility and the Greeks, and visualizes the surface.")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Define the cached fetch function
@st.cache_data(ttl=300)
def fetch_options_data(ticker: str):
    response = requests.get(f"{BACKEND_URL}/api/iv-surface/{ticker}")
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.json().get('detail', 'Unknown error')}")
    data = response.json()
    if not data:
        raise Exception("No valid options data found for this ticker.")
    return pd.DataFrame(data)

col1, col2 = st.columns([1, 1])
with col1:
    popular_tickers = {
        # Major ETFs
        "SPY": "SPDR S&P 500 ETF Trust",
        "QQQ": "Invesco QQQ Trust",
        "IWM": "iShares Russell 2000 ETF",
        "DIA": "SPDR Dow Jones Industrial Average ETF",
        "GLD": "SPDR Gold Shares",
        "TLT": "iShares 20+ Year Treasury Bond ETF",
        "XLF": "Financial Select Sector SPDR Fund",
        "XLK": "Technology Select Sector SPDR Fund",
        "XLE": "Energy Select Sector SPDR Fund",
        "XLV": "Health Care Select Sector SPDR Fund",
        
        # Mega-Cap & Technology
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "NVDA": "NVIDIA Corporation",
        "TSLA": "Tesla, Inc.",
        "AMZN": "Amazon.com, Inc.",
        "META": "Meta Platforms, Inc.",
        "GOOGL": "Alphabet Inc.",
        "AMD": "Advanced Micro Devices, Inc.",
        "INTC": "Intel Corporation",
        "NFLX": "Netflix, Inc.",
        "CRM": "Salesforce, Inc.",
        "ADBE": "Adobe Inc.",
        "CSCO": "Cisco Systems, Inc.",
        "ORCL": "Oracle Corporation",
        "AVGO": "Broadcom Inc.",
        "QCOM": "QUALCOMM Incorporated",
        
        # Financials
        "JPM": "JPMorgan Chase & Co.",
        "BAC": "Bank of America Corp",
        "C": "Citigroup Inc.",
        "WFC": "Wells Fargo & Company",
        "GS": "The Goldman Sachs Group, Inc.",
        "MS": "Morgan Stanley",
        "V": "Visa Inc.",
        "MA": "Mastercard Incorporated",
        "AXP": "American Express Company",
        "SCHW": "The Charles Schwab Corporation",
        
        # Consumer & Retail
        "WMT": "Walmart Inc.",
        "TGT": "Target Corporation",
        "HD": "The Home Depot, Inc.",
        "LOW": "Lowe's Companies, Inc.",
        "MCD": "McDonald's Corporation",
        "SBUX": "Starbucks Corporation",
        "NKE": "NIKE, Inc.",
        "KO": "The Coca-Cola Company",
        "PEP": "PepsiCo, Inc.",
        "PG": "The Procter & Gamble Company",
        "COST": "Costco Wholesale Corporation",
        "DIS": "The Walt Disney Company",
        
        # Healthcare
        "JNJ": "Johnson & Johnson",
        "UNH": "UnitedHealth Group Incorporated",
        "PFE": "Pfizer Inc.",
        "MRK": "Merck & Co., Inc.",
        "ABBV": "AbbVie Inc.",
        "LLY": "Eli Lilly and Company",
        "AMGN": "Amgen Inc.",
        "BMY": "Bristol-Myers Squibb Company",
        
        # Energy & Industrials
        "XOM": "Exxon Mobil Corporation",
        "CVX": "Chevron Corporation",
        "COP": "ConocoPhillips",
        "BA": "The Boeing Company",
        "LMT": "Lockheed Martin Corporation",
        "GE": "General Electric Company",
        "CAT": "Caterpillar Inc.",
        
        # Telecom & Media
        "T": "AT&T Inc.",
        "VZ": "Verizon Communications Inc.",
        "CMCSA": "Comcast Corporation",
        
        # High-Growth / Volatile (Great for IV surfaces)
        "PLTR": "Palantir Technologies Inc.",
        "UBER": "Uber Technologies, Inc.",
        "ABNB": "Airbnb, Inc.",
        "COIN": "Coinbase Global, Inc.",
        "HOOD": "Robinhood Markets, Inc.",
        "SOFI": "SoFi Technologies, Inc.",
        "SQ": "Block, Inc.",
        "PYPL": "PayPal Holdings, Inc.",
        "ROKU": "Roku, Inc."
    }
    
    # Format function to display 'TICKER - Company Name'
    format_ticker = lambda x: f"{x} - {popular_tickers[x]}"
    
    ticker = st.selectbox(
        "Select Stock Ticker Symbol:", 
        options=list(popular_tickers.keys()), 
        format_func=format_ticker,
        index=0
    )
with col2:
    metric_options = {
        'Implied Volatility': 'iv',
        'Delta': 'Delta',
        'Gamma': 'Gamma',
        'Theta': 'Theta',
        'Vega': 'Vega',
        'Rho': 'Rho'
    }
    
    metric_help = '''
    **Quick Reference:**
    - **Implied Volatility:** The market's forecast of a likely movement in the security's price.
    - **Delta:** Expected change in option price for a $1 change in the underlying stock.
    - **Gamma:** The rate of change in Delta (how fast Delta changes).
    - **Theta:** Time decay; how much value the option loses each day.
    - **Vega:** Sensitivity to a 1% change in implied volatility.
    - **Rho:** Sensitivity to changes in the risk-free interest rate.
    '''
    selected_metric = st.selectbox("Select Z-Axis Metric:", list(metric_options.keys()), help=metric_help)

st.markdown("---")

if st.button("Generate Surface", type="primary"):
    with st.spinner(f"Fetching options data & calculating metrics for {ticker}..."):
        try:
            df = fetch_options_data(ticker)
            
            st.success(f"Successfully loaded {len(df)} option contracts!")
            
            # Map selected metric to column name
            z_col = metric_options[selected_metric]
            
            if z_col not in df.columns:
                st.error(f"{selected_metric} is not available in the data.")
            else:
                # Create the Meshgrid
                # We need 2D arrays for Plotly 3D surface
                x = df['strike'].values
                y = df['T'].values
                z = df[z_col].values
                
                # Create a grid to interpolate over
                x_grid = np.linspace(x.min(), x.max(), 100)
                y_grid = np.linspace(y.min(), y.max(), 100)
                X, Y = np.meshgrid(x_grid, y_grid)
                
                # Interpolate Z values
                Z = griddata((x, y), z, (X, Y), method='linear')
                
                # Plotly Rendering
                fig = go.Figure(data=[go.Surface(
                    z=Z, x=X, y=Y, colorscale='Plasma',
                    colorbar=dict(title=selected_metric)
                )])
                
                fig.update_layout(
                    title=f'{selected_metric} Surface for {ticker.upper()}',
                    scene=dict(
                        xaxis_title='Strike Price',
                        yaxis_title='Time to Expiration (Years)',
                        zaxis_title=selected_metric,
                        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)'),
                        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)'),
                        zaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)')
                    ),
                    autosize=False,
                    width=1000,
                    height=800,
                    margin=dict(l=65, r=50, b=65, t=90),
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("Show Raw Data"):
                    st.dataframe(df, use_container_width=True)
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")
