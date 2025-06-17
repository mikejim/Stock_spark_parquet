import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import glob
import os

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Live Stock Prices"

# Helper function to load all Parquet files into a DataFrame
def load_data():
    files = glob.glob("/app/shared_volume/parquet_output/*.parquet")
    if not files:
        return pd.DataFrame()
    try:
        df = pd.concat([pd.read_parquet(f) for f in files])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df.sort_values('timestamp')
    except Exception as e:
        print(f"[dash] Error reading parquet: {e}")
        return pd.DataFrame()

# Layout of the dashboard
app.layout = html.Div([
    html.H1("📈 Live Stock Prices Dashboard"),
    dcc.Interval(id='interval', interval=10000, n_intervals=0),  # Refresh every 10 seconds
    dcc.Dropdown(
        id='symbol-selector',
        options=[],
        value=None,
        placeholder="Select a stock ticker"
    ),
    dcc.Graph(id='line-chart')
])

# Callback to update dropdown options and set default selection
@app.callback(
    Output('symbol-selector', 'options'),
    Output('symbol-selector', 'value'),
    Input('interval', 'n_intervals')
)
def update_dropdown(n):
    df = load_data()
    symbols = sorted(df['symbol'].unique()) if not df.empty else []
    options = [{'label': sym, 'value': sym} for sym in symbols]
    default = options[0]['value'] if options else None
    return options, default

# Callback to update the line chart based on selected symbol
@app.callback(
    Output('line-chart', 'figure'),
    Input('symbol-selector', 'value'),
    Input('interval', 'n_intervals')
)
def update_chart(selected_symbol, n):
    df = load_data()
    if df.empty or not selected_symbol:
        return {
            "layout": {
                "title": "Waiting for data...",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Price (USD)"}
            }
        }
    filtered = df[df['symbol'] == selected_symbol]
    fig = {
        'data': [{
            'x': filtered['timestamp'],
            'y': filtered['price'],
            'type': 'line',
            'name': selected_symbol
        }],
        'layout': {
            'title': f"Live Price - {selected_symbol}",
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Price (USD)'},
            'margin': {'l': 60, 'r': 20, 't': 50, 'b': 40},
            'height': 500
        }
    }
    return fig

# Run the app on 0.0.0.0 so it's accessible from the host machine
if __name__ == '__main__':
#    app.run_server(debug=True, host='0.0.0.0', port=8050)
    app.run(debug=True, host='0.0.0.0', port=8050)
