# ShowStock

A small Dash app that displays historical stock price and volume for a given ticker using `yfinance`.

## Demo

<video autoplay muted loop width="800">
  <source src="https://github.com/rsheitz2/ShowStock/raw/master/assets/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

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
