import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import os


def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Fetch historical stock price data from yfinance, with caching to data folder."""
    ticker = ticker.upper().strip()
    if not ticker:
        raise ValueError("Ticker must be provided")
    
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f"{ticker}.csv")
    
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path, parse_dates=['Date'])
        existing_start = existing_df['Date'].min()
        existing_end = existing_df['Date'].max()
        
        # Check if we need to fetch more data
        fetch_start = start
        fetch_end = end
        need_fetch = False
        
        if pd.to_datetime(start) < existing_start:
            fetch_start = start
            fetch_end = (existing_start - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
            need_fetch = True
        if pd.to_datetime(end) > existing_end:
            if need_fetch:
                # Already fetching, extend end
                fetch_end = end
            else:
                fetch_start = (existing_end + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                fetch_end = end
                need_fetch = True
        
        if need_fetch:
            new_df = yf.download(ticker, start=fetch_start, end=fetch_end, progress=False)
            if not new_df.empty:
                new_df = new_df.reset_index()
                # Flatten columns
                new_df.columns = [col[0] for col in new_df.columns]
                # Append new data to existing
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                # Remove duplicates based on Date
                combined_df = combined_df.drop_duplicates(subset='Date').sort_values('Date')
                combined_df.to_csv(file_path, index=False)
                df = combined_df
            else:
                df = existing_df
        else:
            df = existing_df
    else:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty:
            raise ValueError(f"No data found for ticker={ticker} in the given range")
        df = df.reset_index()
        # Flatten columns
        df.columns = [col[0] for col in df.columns]
        df.to_csv(file_path, index=False)
    
    # Now filter to the requested range
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    df['Date'] = pd.to_datetime(df['Date'])
    filtered_df = df[(df['Date'] >= start_dt) & (df['Date'] <= end_dt)]
    
    if filtered_df.empty:
        raise ValueError(f"No data found for ticker={ticker} in the given range")
    
    return filtered_df


def fig_setup(fig):
    fig.update_layout(plot_bgcolor='white')
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        showgrid=False
    )


app = dash.Dash(__name__)
app.title = "ShowStock"

app.layout = html.Div(
    [
        html.H1("ShowStock: Stock Price + Volume"),
        html.Div(
            [
                html.Label("Ticker"),
                dcc.Input(id="ticker-input", type="text", value="AAPL", style={"width": "120px"}),
                html.Label("Start"),
                dcc.DatePickerSingle(id="start-date", date="2025-01-01"),
                html.Label("End"),
                dcc.DatePickerSingle(id="end-date", date="2025-12-31"),
                html.Button("Load", id="load-button", n_clicks=0),
            ],
            style={"display": "flex", "gap": "10px", "alignItems": "center"},
        ),
        html.Div(id="status", style={"marginTop": "10px", "color": "red"}),
        dcc.Graph(id="price-graph"),
        dcc.Graph(id="volume-graph"),
    ],
    style={"maxWidth": "960px", "margin": "auto", "padding": "20px"},
)


@app.callback(
    [Output("price-graph", "figure"), Output("volume-graph", "figure"), Output("status", "children")],
    [Input("load-button", "n_clicks")],
    [State("ticker-input", "value"), State("start-date", "date"), State("end-date", "date")],
)
def update_graphs(n_clicks, ticker, start_date, end_date):
    if n_clicks is None or n_clicks == 0:
        return {}, {}, ""

    try:
        df = fetch_stock_data(ticker.strip(), start_date, end_date)
    except Exception as e:
        return {}, {}, str(e)

    price_fig = go.Figure()
    fig_setup(price_fig)
    price_fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode='markers', name="Close"))
    price_fig.add_trace(go.Scatter(x=df["Date"], y=df["Open"], mode='markers', name="Open"))
    price_fig.update_layout(title=f"{ticker.upper()} Price")
    price_fig.update_yaxes(title='Price ($)')

    volume_fig = go.Figure()
    fig_setup(volume_fig)
    volume_fig.add_trace(go.Bar(x=df["Date"], y=df["Volume"], name="Volume"))
    volume_fig.update_layout(title=f"{ticker.upper()} Volume")
    volume_fig.update_yaxes(title='Volume')

    return price_fig, volume_fig, ""


if __name__ == "__main__":
    app.run(debug=True)
