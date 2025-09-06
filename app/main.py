import os
import pandas as pd

from polygon import RESTClient

client = RESTClient(api_key=os.getenv("POLYGON_API_KEY"))

# Define the ETF ticker
# Fetch daily historical bars
bars = client.get_aggs(
    ticker="LQD",
    multiplier=1,
    timespan="month",
    from_="2023-01-01",
    to="2025-12-31",
    limit=5000
)

# Convert to DataFrame
df = pd.DataFrame([bar.__dict__ for bar in bars])

# Convert timestamp to readable date
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

print(df)