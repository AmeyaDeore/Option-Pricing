import numpy as np
from scipy.stats import norm
import pandas as pd

def calculate_d1_d2(S, K, T, r, q, sigma):
    # Add a small epsilon to T and sigma to prevent division by zero
    T = np.maximum(T, 1e-10)
    sigma = np.maximum(sigma, 1e-10)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def bs_price(S, K, T, r, q, sigma, option_type='call'):
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    
    is_call = (option_type == 'call')
    
    call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    
    return np.where(is_call, call_price, put_price)

def bs_vega(S, K, T, r, q, sigma):
    d1, _ = calculate_d1_d2(S, K, T, r, q, sigma)
    vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)
    return vega

def calculate_greeks(S, K, T, r, q, sigma, option_type='call'):
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    is_call = (option_type == 'call')
    
    # Delta
    call_delta = np.exp(-q * T) * norm.cdf(d1)
    put_delta = -np.exp(-q * T) * norm.cdf(-d1)
    delta = np.where(is_call, call_delta, put_delta)
    
    # Gamma (same for call/put)
    gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T) + 1e-10)
    
    # Theta
    common_theta = -(S * np.exp(-q * T) * norm.pdf(d1) * sigma) / (2 * np.sqrt(T) + 1e-10)
    call_theta = common_theta - r * K * np.exp(-r * T) * norm.cdf(d2) + q * S * np.exp(-q * T) * norm.cdf(d1)
    put_theta = common_theta + r * K * np.exp(-r * T) * norm.cdf(-d2) - q * S * np.exp(-q * T) * norm.cdf(-d1)
    theta = np.where(is_call, call_theta, put_theta)
    
    # Vega
    vega = bs_vega(S, K, T, r, q, sigma)
    
    # Rho
    call_rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    put_rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    rho = np.where(is_call, call_rho, put_rho)
    
    return delta, gamma, theta, vega, rho

def calculate_iv(S, K, T, r, q, market_price, option_type='call'):
    """
    Vectorized Implied Volatility calculation using Newton-Raphson.
    Input parameters should be numpy arrays.
    """
    K = np.asarray(K)
    S = np.asarray(S)
    if S.ndim == 0:
        S = np.full_like(K, S, dtype=float)
    T = np.asarray(T)
    market_price = np.asarray(market_price)
    option_type = np.asarray(option_type)
    
    MAX_ITERATIONS = 100
    TOLERANCE = 1e-4

    sigma = np.full_like(S, 0.5, dtype=float)  # Initial guess (50%)
    
    # Intrinsic value bounds
    is_call = (option_type == 'call')
    intrinsic_call = np.maximum(0, S - K)
    intrinsic_put = np.maximum(0, K - S)
    intrinsic = np.where(is_call, intrinsic_call, intrinsic_put)
    
    # Valid mask: we only optimize where market price > intrinsic value
    valid_mask = market_price > intrinsic
    active_mask = valid_mask.copy()
    
    for i in range(MAX_ITERATIONS):
        if not np.any(active_mask):
            break
            
        S_active = S[active_mask]
        K_active = K[active_mask]
        T_active = T[active_mask]
        market_price_active = market_price[active_mask]
        sigma_active = sigma[active_mask]
        
        opt_type_active = option_type[active_mask]
            
        price = bs_price(S_active, K_active, T_active, r, q, sigma_active, opt_type_active)
        vega = bs_vega(S_active, K_active, T_active, r, q, sigma_active)
        
        diff = price - market_price_active
        converged = np.abs(diff) < TOLERANCE
        small_vega = vega < 1e-6
        stop_mask = converged | small_vega
        update_mask = ~stop_mask
        
        if np.any(update_mask):
            sigma_active[update_mask] = sigma_active[update_mask] - (diff[update_mask] / vega[update_mask])
            sigma_active[update_mask] = np.maximum(sigma_active[update_mask], 1e-4)
            
        sigma[active_mask] = sigma_active
        active_indices = np.nonzero(active_mask)[0]
        active_mask[active_indices[stop_mask]] = False
        
    # Return NaN for invalid options
    sigma[~valid_mask] = np.nan
    return sigma
