import requests
import dotenv
import os
import json
import pandas as pd
from datetime import datetime

dotenv.load_dotenv()

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

headers = {
    'Content-Type': 'application/json'
}

ticker = "AAPL"

# Create output directory if it doesn't exist
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# 1. Get available fundamental metrics definitions
print("=" * 50)
print("1. Fundamental Metrics Definitions")
print("=" * 50)
definitions_response = requests.get(
    f"https://api.tiingo.com/tiingo/fundamentals/definitions?token={TIINGO_API_KEY}",
    headers=headers
)
definitions_data = definitions_response.json()
print(f"Retrieved {len(definitions_data)} definitions")

# Save as JSON
definitions_file = f"{output_dir}/definitions.json"
with open(definitions_file, 'w', encoding='utf-8') as f:
    json.dump(definitions_data, f, indent=2, ensure_ascii=False)
print(f"✓ Saved to {definitions_file}")

# 2. Get historical statement data
print("\n" + "=" * 50)
print(f"2. Historical Statement Data for {ticker}")
print("=" * 50)
statements_response = requests.get(
    f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/statements?token={TIINGO_API_KEY}",
    headers=headers
)
statements_data = statements_response.json()
print(f"Retrieved statement data for {ticker}")

# Save as JSON
statements_json_file = f"{output_dir}/{ticker}_statements.json"
with open(statements_json_file, 'w', encoding='utf-8') as f:
    json.dump(statements_data, f, indent=2, ensure_ascii=False)
print(f"✓ Saved to {statements_json_file}")

# Convert to DataFrame and save as CSV if data is available
if statements_data:
    df_statements = pd.DataFrame(statements_data)
    statements_csv_file = f"{output_dir}/{ticker}_statements.csv"
    df_statements.to_csv(statements_csv_file, index=False, encoding='utf-8')
    print(f"✓ Saved to {statements_csv_file}")

# 3. Get historical daily fundamental data
print("\n" + "=" * 50)
print(f"3. Historical Daily Fundamental Data for {ticker}")
print("=" * 50)
daily_response = requests.get(
    f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/daily?token={TIINGO_API_KEY}",
    headers=headers
)
daily_data = daily_response.json()
print(f"Retrieved daily fundamental data for {ticker}")

# Save as JSON
daily_json_file = f"{output_dir}/{ticker}_daily.json"
with open(daily_json_file, 'w', encoding='utf-8') as f:
    json.dump(daily_data, f, indent=2, ensure_ascii=False)
print(f"✓ Saved to {daily_json_file}")

# Convert to DataFrame and save as CSV if data is available
if daily_data:
    df_daily = pd.DataFrame(daily_data)
    daily_csv_file = f"{output_dir}/{ticker}_daily.csv"
    df_daily.to_csv(daily_csv_file, index=False, encoding='utf-8')
    print(f"✓ Saved to {daily_csv_file}")

# 4. Get fundamental meta data
print("\n" + "=" * 50)
print("4. Fundamental Meta Data")
print("=" * 50)
meta_response = requests.get(
    f"https://api.tiingo.com/tiingo/fundamentals/meta?token={TIINGO_API_KEY}",
    headers=headers
)
meta_data = meta_response.json()
print(f"Retrieved meta data")

# Save as JSON
meta_file = f"{output_dir}/meta.json"
with open(meta_file, 'w', encoding='utf-8') as f:
    json.dump(meta_data, f, indent=2, ensure_ascii=False)
print(f"✓ Saved to {meta_file}")

print("\n" + "=" * 50)
print("All data saved successfully!")
print("=" * 50)
