# Risk Analytics Dashboard

An interactive web-based dashboard for analyzing and visualizing portfolio risk metrics.

## Features

- Portfolio Value Tracking
- Risk Metrics Visualization
  - Value at Risk (VaR)
  - Expected Shortfall (ES)
  - Correlation Analysis
  - Rolling Volatility
- Interactive Controls
  - Adjustable Confidence Levels
  - Customizable Time Windows

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mj2603/risk-analytics-dashboard.git
cd risk-analytics-dashboard
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard:
```bash
python main.py
```

The dashboard will be available at http://127.0.0.1:8050/

## Project Structure

```
risk-analytics-dashboard/
├── src/
│   ├── analytics/
│   │   └── risk_metrics.py
│   ├── visualization/
│   │   └── dashboard.py
│   └── utils/
├── data/
├── tests/
├── notebooks/
├── docs/
├── main.py
└── requirements.txt
```

## Dependencies

- pandas >= 1.5.0
- numpy >= 1.21.0
- plotly >= 5.13.0
- dash >= 2.9.0
- scipy >= 1.9.0
- scikit-learn >= 1.0.0
- yfinance >= 0.2.0
- matplotlib >= 3.5.0
- seaborn >= 0.12.0
- statsmodels >= 0.13.0
- arch >= 5.0.0

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 