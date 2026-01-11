import requests
import dotenv
import os
import json

dotenv.load_dotenv()

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

headers = {
        'Content-Type': 'application/json'
        }

ticker = "AAPL"
startDate = "2025-01-11"
endDate = "2026-01-11"

requestResponse = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={startDate}&endDate={endDate}&token={TIINGO_API_KEY}",
                                    headers=headers)

data = requestResponse.json()
print(data)

# JSON 파일로 저장
output_file = f"{ticker}_prices_{startDate.replace('-', '')}_{endDate.replace('-', '')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n결과가 {output_file}에 저장되었습니다.")