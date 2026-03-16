# ShowStock

A small Dash app that displays historical stock price and volume for a given ticker using `yfinance`.

## Demo

https://github.com/rsheitz2/ShowStock/blob/master/assets/demo.mp4

## Setup

```bash
cd ShowStock
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open http://127.0.0.1:8050 in your browser.

## Usage

- Enter a stock ticker (e.g. `AAPL`, `MSFT`, `GOOG`)
- Choose a start/end date
- Click **Load** to refresh charts
