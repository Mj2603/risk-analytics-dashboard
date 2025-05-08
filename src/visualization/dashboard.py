"""
Interactive Risk Analytics Dashboard

This module creates an interactive web-based dashboard for risk analytics using Dash and Plotly.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Union
import yfinance as yf
from datetime import datetime, timedelta

class RiskDashboard:
    """
    Interactive dashboard for risk analytics visualization.
    
    This class creates a web-based dashboard with:
    - Risk metrics visualization
    - Portfolio analytics
    - Interactive charts
    - Real-time updates
    """
    
    def __init__(self, portfolio_data: Union[pd.DataFrame, str]):
        """
        Initialize the RiskDashboard.
        
        Args:
            portfolio_data: DataFrame with portfolio data or path to CSV file
        """
        self.portfolio_data = portfolio_data
        self.returns = portfolio_data.pct_change().dropna()
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        """Set up the dashboard layout."""
        self.app.layout = html.Div([
            html.H1("Risk Analytics Dashboard", style={'textAlign': 'center'}),
            
            # Portfolio Overview
            html.Div([
                html.H2("Portfolio Overview"),
                dcc.Graph(id='portfolio-value-chart'),
                dcc.Graph(id='returns-distribution')
            ]),
            
            # Risk Metrics
            html.Div([
                html.H2("Risk Metrics"),
                html.Div([
                    html.Div([
                        html.H3("Value at Risk (VaR)"),
                        dcc.Graph(id='var-chart')
                    ], className='six columns'),
                    html.Div([
                        html.H3("Expected Shortfall (ES)"),
                        dcc.Graph(id='es-chart')
                    ], className='six columns')
                ], className='row'),
                
                html.Div([
                    html.Div([
                        html.H3("Correlation Matrix"),
                        dcc.Graph(id='correlation-matrix')
                    ], className='six columns'),
                    html.Div([
                        html.H3("Rolling Volatility"),
                        dcc.Graph(id='rolling-volatility')
                    ], className='six columns')
                ], className='row')
            ]),
            
            # Controls
            html.Div([
                html.H3("Controls"),
                html.Div([
                    html.Label("Confidence Level:"),
                    dcc.Slider(
                        id='confidence-slider',
                        min=90,
                        max=99,
                        step=1,
                        value=95,
                        marks={i: f'{i}%' for i in range(90, 100, 1)}
                    )
                ]),
                html.Div([
                    html.Label("Window Size:"),
                    dcc.Slider(
                        id='window-slider',
                        min=20,
                        max=252,
                        step=1,
                        value=60,
                        marks={i: f'{i}d' for i in [20, 60, 120, 252]}
                    )
                ])
            ])
        ])
        
    def setup_callbacks(self):
        """Set up dashboard callbacks for interactivity."""
        
        @self.app.callback(
            [Output('portfolio-value-chart', 'figure'),
             Output('returns-distribution', 'figure'),
             Output('var-chart', 'figure'),
             Output('es-chart', 'figure'),
             Output('correlation-matrix', 'figure'),
             Output('rolling-volatility', 'figure')],
            [Input('confidence-slider', 'value'),
             Input('window-slider', 'value')]
        )
        def update_charts(confidence_level, window_size):
            # Portfolio Value Chart
            portfolio_value = self.portfolio_data.mean(axis=1)
            portfolio_fig = go.Figure()
            portfolio_fig.add_trace(go.Scatter(
                x=portfolio_value.index,
                y=portfolio_value,
                mode='lines',
                name='Portfolio Value'
            ))
            portfolio_fig.update_layout(
                title='Portfolio Value Over Time',
                xaxis_title='Date',
                yaxis_title='Value'
            )
            
            # Returns Distribution
            returns_fig = go.Figure()
            for col in self.returns.columns:
                returns_fig.add_trace(go.Histogram(
                    x=self.returns[col],
                    name=col,
                    opacity=0.7
                ))
            returns_fig.update_layout(
                title='Returns Distribution',
                xaxis_title='Return',
                yaxis_title='Frequency',
                barmode='overlay'
            )
            
            # VaR Chart
            var = self.returns.quantile(1 - confidence_level/100)
            var_fig = go.Figure()
            var_fig.add_trace(go.Bar(
                x=var.index,
                y=var.values,
                name='VaR'
            ))
            var_fig.update_layout(
                title=f'{confidence_level}% Value at Risk',
                xaxis_title='Asset',
                yaxis_title='VaR'
            )
            
            # ES Chart
            es = self.returns[self.returns <= var].mean()
            es_fig = go.Figure()
            es_fig.add_trace(go.Bar(
                x=es.index,
                y=es.values,
                name='ES'
            ))
            es_fig.update_layout(
                title=f'{confidence_level}% Expected Shortfall',
                xaxis_title='Asset',
                yaxis_title='ES'
            )
            
            # Correlation Matrix
            corr = self.returns.corr()
            corr_fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='RdBu'
            ))
            corr_fig.update_layout(
                title='Correlation Matrix',
                xaxis_title='Asset',
                yaxis_title='Asset'
            )
            
            # Rolling Volatility
            rolling_vol = self.returns.rolling(window=window_size).std() * np.sqrt(252)
            vol_fig = go.Figure()
            for col in rolling_vol.columns:
                vol_fig.add_trace(go.Scatter(
                    x=rolling_vol.index,
                    y=rolling_vol[col],
                    name=col,
                    mode='lines'
                ))
            vol_fig.update_layout(
                title=f'{window_size}-Day Rolling Volatility',
                xaxis_title='Date',
                yaxis_title='Volatility'
            )
            
            return portfolio_fig, returns_fig, var_fig, es_fig, corr_fig, vol_fig
    
    def run(self, debug: bool = True, port: int = 8050):
        """
        Run the dashboard.
        
        Args:
            debug: Enable debug mode
            port: Port number for the dashboard
        """
        self.app.run(debug=debug, port=port)

if __name__ == "__main__":
    # Example usage
    portfolio_data = pd.DataFrame({
        'AAPL': yf.download('AAPL', start='2020-01-01', end='2023-12-31')['Adj Close'],
        'MSFT': yf.download('MSFT', start='2020-01-01', end='2023-12-31')['Adj Close'],
        'GOOGL': yf.download('GOOGL', start='2020-01-01', end='2023-12-31')['Adj Close']
    })
    
    dashboard = RiskDashboard(portfolio_data)
    dashboard.run() 