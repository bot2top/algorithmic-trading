import pandas as pd
import requests

def fetch_sp500_wikipedia() -> pd.DataFrame:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    # Wikipedia는 User-Agent 헤더가 필요함
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    # requests로 HTML 가져오기
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # pandas로 파싱
    df = pd.read_html(response.text)[0]
    df["Symbol"] = df["Symbol"].str.strip()
    return df

df = fetch_sp500_wikipedia()
tickers = df["Symbol"].tolist()
print(len(tickers), tickers[:20])

import datetime

def save_tickers_to_file(tickers: list[str]) -> None:
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"snp500_tickers_{today_str}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for ticker in tickers:
            f.write(f"{ticker}\n")

save_tickers_to_file(tickers)
