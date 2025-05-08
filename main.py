"""
Main entry point for the Risk Analytics Dashboard
"""

import pandas as pd
import yfinance as yf
from src.visualization.dashboard import RiskDashboard

def main():
    # Example portfolio data
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    
    # Download data
    portfolio_data = pd.DataFrame()
    for symbol in symbols:
        data = yf.download(symbol, start='2020-01-01', end='2023-12-31')
        if 'Adj Close' in data.columns:
            portfolio_data[symbol] = data['Adj Close']
        else:
            portfolio_data[symbol] = data['Close']
    
    # Initialize and run dashboard
    dashboard = RiskDashboard(portfolio_data)
    dashboard.run()

if __name__ == "__main__":
    main()