"""
S&P 500 종목 중 2025년 0분기(연간) fundamental 데이터 수집
- Tiingo API를 사용하여 fundamental statements 데이터 조회
- 2025년 quarter=0 데이터가 존재하는 종목만 필터링
- 결과를 CSV 파일로 저장
"""

import requests
import dotenv
import os
import json
import pandas as pd
from datetime import datetime
from io import StringIO
import time

dotenv.load_dotenv()

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

headers = {
    'Content-Type': 'application/json'
}

# Output directory
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)


def fetch_sp500_tickers() -> list[str]:
    """Wikipedia에서 S&P 500 티커 리스트 가져오기"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    df = pd.read_html(StringIO(response.text))[0]
    df["Symbol"] = df["Symbol"].str.strip()
    # BRK.B -> BRK-B 형태로 변환 (Tiingo API 호환)
    df["Symbol"] = df["Symbol"].str.replace(".", "-", regex=False)
    return df["Symbol"].tolist()


def get_fundamental_statements(ticker: str) -> list[dict]:
    """특정 티커의 fundamental statements 데이터 조회"""
    try:
        response = requests.get(
            f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/statements?token={TIINGO_API_KEY}",
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  Warning: {ticker} - Status {response.status_code}")
            return []
    except Exception as e:
        print(f"  Error fetching {ticker}: {e}")
        return []


def extract_statement_data(statement: dict) -> dict:
    """statementData를 평면화하여 단일 딕셔너리로 변환"""
    result = {
        'date': statement.get('date'),
        'year': statement.get('year'),
        'quarter': statement.get('quarter')
    }

    statement_data = statement.get('statementData', {})

    # 각 재무제표 유형별로 데이터 추출
    for statement_type in ['balanceSheet', 'incomeStatement', 'cashFlow', 'overview']:
        items = statement_data.get(statement_type, [])
        for item in items:
            data_code = item.get('dataCode')
            value = item.get('value')
            if data_code:
                result[data_code] = value

    return result


def main():
    print("=" * 60)
    print("S&P 500 Fundamentals - 2025 Q0 Data Collection")
    print("=" * 60)

    # 1. S&P 500 티커 가져오기
    print("\n[1/3] Fetching S&P 500 tickers...")
    tickers = fetch_sp500_tickers()
    print(f"  Found {len(tickers)} tickers")

    # 2. 각 티커에 대해 fundamental 데이터 조회
    print("\n[2/3] Fetching fundamental data for each ticker...")

    all_data = []
    tickers_with_q0 = []

    for i, ticker in enumerate(tickers):
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i + 1}/{len(tickers)}")

        statements = get_fundamental_statements(ticker)

        # 2025년 Q0 데이터 필터링
        for stmt in statements:
            if stmt.get('year') == 2025 and stmt.get('quarter') == 0:
                flat_data = extract_statement_data(stmt)
                flat_data['ticker'] = ticker
                all_data.append(flat_data)
                tickers_with_q0.append(ticker)
                break

        # API rate limit 고려 (초당 요청 제한)
        time.sleep(0.1)

    print(f"\n  Completed! Found {len(all_data)} tickers with 2025 Q0 data")

    # 3. 결과 저장
    print("\n[3/3] Saving results...")

    if all_data:
        df = pd.DataFrame(all_data)

        # ticker를 첫 번째 컬럼으로 이동
        cols = ['ticker', 'date', 'year', 'quarter'] + [c for c in df.columns if c not in ['ticker', 'date', 'year', 'quarter']]
        df = df[cols]

        # 날짜 정보로 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # CSV 저장
        csv_file = f"{output_dir}/snp500_fundamentals_2025Q0_{timestamp}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"  Saved to {csv_file}")

        # JSON 저장 (원본 데이터)
        json_file = f"{output_dir}/snp500_fundamentals_2025Q0_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print(f"  Saved to {json_file}")

        # 티커 리스트 저장
        tickers_file = f"{output_dir}/tickers_with_2025Q0_{timestamp}.txt"
        with open(tickers_file, 'w', encoding='utf-8') as f:
            for t in tickers_with_q0:
                f.write(f"{t}\n")
        print(f"  Saved ticker list to {tickers_file}")

        # 요약 출력
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"  Total S&P 500 tickers: {len(tickers)}")
        print(f"  Tickers with 2025 Q0 data: {len(all_data)}")
        print(f"  Columns in output: {len(df.columns)}")
        print(f"\nSample tickers: {tickers_with_q0[:10]}")
    else:
        print("  No data found for 2025 Q0. Checking available quarters...")

        # 데이터가 없으면 첫 번째 티커에서 사용 가능한 분기 확인
        sample_ticker = tickers[0] if tickers else "AAPL"
        statements = get_fundamental_statements(sample_ticker)
        if statements:
            available = [(s.get('year'), s.get('quarter')) for s in statements[:10]]
            print(f"  Available periods for {sample_ticker}: {available}")


if __name__ == "__main__":
    main()
