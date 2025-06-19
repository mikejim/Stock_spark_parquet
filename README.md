# Stock Spark Streaming to Parquet with Dash Visualization

This project streams real-time stock prices (AAPL, MSFT, GOOG) from Financial Modeling Prep API, processes them using Spark Structured Streaming, saves them in Parquet format, and visualizes them in a Dash web UI.

## Stack
- Python (Producer + Dash)
- Apache Spark (Structured Streaming)
- Parquet file format
- Docker & Docker Compose

## Folder Structure
- `producer/`: pulls stock data and sends to a socket
- `spark/`: Spark job to read socket and write Parquet
- `dash/`: Dash app for visualizing live prices
- `shared_volume/`: shared Docker volume for Parquet files

## How to Run

1. Get a free API key from [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs)
2. Add it to `docker-compose.yml` under `API_KEY`
3. Start the project:
   ```bash
   docker-compose up --build
   ```
4. Visit the dashboard at [http://localhost:8050](http://localhost:8050)

