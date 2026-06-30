import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from core_math import calculate_iv, calculate_greeks

def get_risk_free_rate():
    try:
        tnx = yf.Ticker("^TNX")
        # TNX is quoted in percentages (e.g. 4.1 means 4.1%)
        hist = tnx.history(period="1d")
        if not hist.empty:
            r = hist['Close'].iloc[0] / 100.0
            return r
    except Exception as e:
        print(f"Warning: Failed to fetch dynamic risk-free rate: {e}")
    return 0.04  # Fallback

def get_options_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    
    # Get the current stock price
    history = ticker.history(period="1d")
    if history.empty:
        raise ValueError(f"Could not fetch stock price for ticker: {ticker_symbol}")
    
    S = history['Close'].iloc[0]
    
    # Get dividend yield
    try:
        q = ticker.info.get('dividendYield', 0.0)
        if q is None:
            q = 0.0
    except:
        q = 0.0
        
    # Get dynamic risk-free rate
    r = get_risk_free_rate()
    
    # Get expirations
    expirations = ticker.options
    if not expirations:
        raise ValueError(f"No options expirations found for ticker: {ticker_symbol}")
    
    valid_contracts = []
    
    for exp in expirations:
        # Calculate time to expiration in years
        exp_date = datetime.strptime(exp, '%Y-%m-%d')
        T = (exp_date - datetime.now()).days / 365.0
        
        if T <= 0:
            continue
            
        try:
            chain = ticker.option_chain(exp)
            
            # Process calls
            calls = chain.calls
            calls = calls[(calls['volume'] > 0) & (calls['bid'] > 0)]
            for _, row in calls.iterrows():
                market_price = (row['bid'] + row['ask']) / 2
                valid_contracts.append({
                    'strike': row['strike'],
                    'T': T,
                    'market_price': market_price,
                    'option_type': 'call'
                })
                
            # Process puts
            puts = chain.puts
            puts = puts[(puts['volume'] > 0) & (puts['bid'] > 0)]
            for _, row in puts.iterrows():
                market_price = (row['bid'] + row['ask']) / 2
                valid_contracts.append({
                    'strike': row['strike'],
                    'T': T,
                    'market_price': market_price,
                    'option_type': 'put'
                })
                
        except Exception as e:
            print(f"Warning: Failed to fetch option chain for {exp}: {e}")
            continue

    if not valid_contracts:
        raise ValueError("No valid contracts found after filtering.")
        
    # Convert to DataFrame
    df = pd.DataFrame(valid_contracts)
    
    # Vectorized IV Calculation
    df['iv'] = calculate_iv(
        S=S,
        K=df['strike'].values,
        T=df['T'].values,
        r=r,
        q=q,
        market_price=df['market_price'].values,
        option_type=df['option_type'].values
    )
    
    # Drop rows where IV could not be calculated (NaN)
    df = df.dropna(subset=['iv'])
    
    # Vectorized Greeks Calculation
    if not df.empty:
        delta, gamma, theta, vega, rho = calculate_greeks(
            S=S,
            K=df['strike'].values,
            T=df['T'].values,
            r=r,
            q=q,
            sigma=df['iv'].values,
            option_type=df['option_type'].values
        )
        
        df['Delta'] = delta
        df['Gamma'] = gamma
        df['Theta'] = theta
        df['Vega'] = vega
        df['Rho'] = rho
    
    return df
