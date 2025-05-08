"""
Risk Metrics Module

This module provides comprehensive risk analytics functionality including:
- Value at Risk (VaR) calculations
- Expected Shortfall (ES)
- Portfolio risk metrics
- Factor risk analysis
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Union, Optional
import yfinance as yf

class RiskMetrics:
    """
    A class for calculating various risk metrics for financial portfolios.
    
    This class implements industry-standard risk metrics including:
    - Value at Risk (VaR)
    - Expected Shortfall (ES)
    - Portfolio Beta
    - Correlation Analysis
    - Factor Risk Decomposition
    """
    
    def __init__(self, 
                 portfolio_data: Union[pd.DataFrame, str],
                 benchmark: str = '^GSPC',
                 risk_free_rate: float = 0.02):
        """
        Initialize the RiskMetrics class.
        
        Args:
            portfolio_data: DataFrame with portfolio returns or path to CSV file
            benchmark: Benchmark ticker symbol (default: S&P 500)
            risk_free_rate: Annual risk-free rate (default: 2%)
        """
        self.risk_free_rate = risk_free_rate
        
        # Load portfolio data
        if isinstance(portfolio_data, str):
            self.portfolio_data = pd.read_csv(portfolio_data, index_col=0, parse_dates=True)
        else:
            self.portfolio_data = portfolio_data
            
        # Load benchmark data
        self.benchmark = benchmark
        self._load_benchmark_data()
        
        # Calculate returns
        self.returns = self.portfolio_data.pct_change().dropna()
        
    def _load_benchmark_data(self):
        """Load benchmark data using yfinance."""
        try:
            benchmark_data = yf.download(self.benchmark, 
                                       start=self.portfolio_data.index[0],
                                       end=self.portfolio_data.index[-1])['Adj Close']
            self.benchmark_returns = benchmark_data.pct_change().dropna()
        except Exception as e:
            print(f"Error loading benchmark data: {e}")
            self.benchmark_returns = pd.Series()
    
    def calculate_var(self, 
                     confidence_level: float = 0.95,
                     method: str = 'historical') -> pd.Series:
        """
        Calculate Value at Risk (VaR) using different methodologies.
        
        Args:
            confidence_level: Confidence level for VaR calculation (default: 95%)
            method: VaR calculation method ('historical', 'parametric', 'monte_carlo')
            
        Returns:
            pd.Series: VaR for each asset
        """
        if method == 'historical':
            return -self.returns.quantile(1 - confidence_level)
        elif method == 'parametric':
            z_score = stats.norm.ppf(confidence_level)
            return -(self.returns.mean() - z_score * self.returns.std())
        elif method == 'monte_carlo':
            n_simulations = 10000
            mu = self.returns.mean()
            sigma = self.returns.std()
            simulated_returns = pd.DataFrame(
                {col: np.random.normal(mu[col], sigma[col], n_simulations)
                 for col in self.returns.columns}
            )
            return -simulated_returns.quantile(1 - confidence_level)
        else:
            raise ValueError("Invalid method. Use historical, parametric, or monte_carlo.")
    
    def calculate_expected_shortfall(self, 
                                   confidence_level: float = 0.95) -> pd.Series:
        """
        Calculate Expected Shortfall (ES) / Conditional VaR.
        
        Args:
            confidence_level: Confidence level for ES calculation (default: 95%)
            
        Returns:
            pd.Series: ES for each asset
        """
        var = self.calculate_var(confidence_level)
        return -self.returns[self.returns <= -var].mean()
    
    def calculate_portfolio_beta(self) -> pd.Series:
        """
        Calculate portfolio beta relative to the benchmark.
        
        Returns:
            pd.Series: Beta for each asset
        """
        betas = pd.Series(index=self.returns.columns)
        for col in self.returns.columns:
            cov = np.cov(self.returns[col], self.benchmark_returns)[0, 1]
            var = np.var(self.benchmark_returns)
            betas[col] = cov / var
        return betas
    
    def calculate_correlation_matrix(self) -> pd.DataFrame:
        """
        Calculate correlation matrix for portfolio assets.
        
        Returns:
            pd.DataFrame: Correlation matrix
        """
        return self.returns.corr()
    
    def calculate_factor_risk(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate factor risk decomposition.
        
        Returns:
            dict: Factor risk metrics
        """
        # Example factors: Market, Size, Value
        factors = {
            "Market": self.benchmark_returns,
            "Size": self.benchmark_returns.rolling(window=60).std(),
            "Value": self.benchmark_returns.rolling(window=252).mean()
        }
        
        factor_returns = pd.DataFrame(factors)
        factor_exposures = {}
        
        for col in self.returns.columns:
            model = stats.linregress(factor_returns["Market"], self.returns[col])
            factor_exposures[col] = {
                "Market_Beta": model.slope,
                "Alpha": model.intercept,
                "R_squared": model.rvalue ** 2
            }
        
        return factor_exposures
    
    def generate_risk_report(self) -> Dict[str, Union[float, pd.DataFrame]]:
        """
        Generate comprehensive risk report.
        
        Returns:
            dict: Risk metrics report
        """
        report = {
            "VaR_95": self.calculate_var(),
            "Expected_Shortfall_95": self.calculate_expected_shortfall(),
            "Portfolio_Beta": self.calculate_portfolio_beta(),
            "Correlation_Matrix": self.calculate_correlation_matrix(),
            "Annualized_Volatility": self.returns.std() * np.sqrt(252),
            "Sharpe_Ratio": (self.returns.mean() * 252 - self.risk_free_rate) / 
                           (self.returns.std() * np.sqrt(252)),
            "Factor_Risk": self.calculate_factor_risk()
        }
        
        return report

if __name__ == "__main__":
    # Example usage
    portfolio_data = pd.DataFrame({
        'AAPL': yf.download('AAPL', start='2020-01-01', end='2023-12-31')['Adj Close'],
        'MSFT': yf.download('MSFT', start='2020-01-01', end='2023-12-31')['Adj Close'],
        'GOOGL': yf.download('GOOGL', start='2020-01-01', end='2023-12-31')['Adj Close']
    })
    
    risk_metrics = RiskMetrics(portfolio_data)
    report = risk_metrics.generate_risk_report()
    
    print("\nRisk Report:")
    for metric, value in report.items():
        if isinstance(value, pd.DataFrame):
            print(f"\n{metric}:")
            print(value)
        else:
            print(f"{metric}: {value:.4f}") 