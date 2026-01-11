import requests
import dotenv
import os
import csv
import argparse
from datetime import datetime, timedelta
from typing import Optional

dotenv.load_dotenv()

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

headers = {
    'Content-Type': 'application/json'
}


def get_price_on_date(ticker: str, date: str, debug: bool = False) -> Optional[float]:
    """특정 날짜 또는 그 이전 가장 최근 거래일의 종목 가격을 조회합니다."""
    try:
        # 해당 날짜가 주말/휴일일 수 있으므로 7일 범위로 조회하여 가장 최근 거래일 데이터 가져오기
        start_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
        
        response = requests.get(
            f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={date}&token={TIINGO_API_KEY}",
            headers=headers
        )
        
        if debug:
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
        
        data = response.json()
        
        if data and len(data) > 0:
            # 가장 최근 거래일 데이터 반환 (배열의 마지막)
            # adjClose: 액면분할, 배당 등이 조정된 가격
            return data[-1]['adjClose']
        
        if debug:
            print(f"  Data: {data}")
        
        return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None


def calculate_return(old_price: float, new_price: float) -> float:
    """수익률을 계산합니다."""
    if old_price == 0:
        return 0
    return ((new_price - old_price) / old_price) * 100


def main():
    # Command line arguments 파싱
    parser = argparse.ArgumentParser(description='주식 1년 수익률 비교 프로그램')
    parser.add_argument('-t', '--tickers', nargs='+', help='비교할 티커 리스트 (예: AAPL MSFT GOOGL)')
    parser.add_argument('-f', '--file', type=str, help='티커 리스트 파일 경로')
    parser.add_argument('-d', '--date', type=str, help='비교 기준 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)')
    
    args = parser.parse_args()
    
    # 날짜 설정
    if args.date:
        current_date_str = args.date
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    else:
        current_date = datetime.now()
        current_date_str = current_date.strftime("%Y-%m-%d")
        print(f"오늘 날짜를 사용합니다: {current_date_str}")
    
    # 1년 전 날짜 계산
    one_year_ago = current_date - timedelta(days=365)
    one_year_ago_str = one_year_ago.strftime("%Y-%m-%d")
    
    print(f"현재 날짜: {current_date_str}")
    print(f"1년 전 날짜: {one_year_ago_str}")
    
    # 티커 리스트 가져오기
    if args.tickers:
        # 명령줄에서 직접 입력받은 티커 사용
        tickers = args.tickers
        print(f"\n입력된 {len(tickers)}개 종목을 조회합니다: {', '.join(tickers)}\n")
    elif args.file:
        # 지정된 파일에서 티커 읽기
        with open(args.file, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
        print(f"\n{args.file}에서 {len(tickers)}개 종목을 읽었습니다.\n")
    else:
        # 기본값: S&P 500 티커 파일
        tickers_file = "../assets/snp500_tickers_20260104.txt"
        with open(tickers_file, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
        print(f"\n기본 S&P 500 리스트에서 {len(tickers)}개 종목을 조회합니다.\n")
    
    # 결과를 저장할 리스트
    results = []
    
    # 각 종목에 대해 가격 조회
    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] {ticker} 조회 중...")
        
        # 첫 번째 종목은 디버그 모드로 실행
        debug_mode = (i == 1)
        
        # 1년 전 가격
        if debug_mode:
            print(f"  1년 전 가격 조회 중 ({one_year_ago_str})...")
        old_price = get_price_on_date(ticker, one_year_ago_str, debug=debug_mode)
        
        # 현재 가격
        if debug_mode:
            print(f"  현재 가격 조회 중 ({current_date_str})...")
        current_price = get_price_on_date(ticker, current_date_str, debug=debug_mode)
        
        if old_price is not None and current_price is not None:
            # 수익률 계산
            return_rate = calculate_return(old_price, current_price)
            
            results.append({
                'ticker': ticker,
                'old_price': old_price,
                'old_date': one_year_ago_str,
                'current_price': current_price,
                'current_date': current_date_str,
                'return_rate': return_rate
            })
            
            print(f"  ✓ 1년 전: ${old_price:.2f}, 현재: ${current_price:.2f}, 수익률: {return_rate:.2f}%")
        else:
            print(f"  ✗ 데이터를 가져올 수 없습니다.")
    
    # CSV 파일로 저장
    output_filename = f"price_comparison_{one_year_ago_str.replace('-', '')}_{current_date_str.replace('-', '')}.csv"
    
    with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['종목명', f'1년 전 가격 ({one_year_ago_str})', f'현재 가격 ({current_date_str})', '수익률 (%)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                '종목명': result['ticker'],
                f'1년 전 가격 ({one_year_ago_str})': f"${result['old_price']:.2f}",
                f'현재 가격 ({current_date_str})': f"${result['current_price']:.2f}",
                '수익률 (%)': f"{result['return_rate']:.2f}%"
            })
    
    print(f"\n완료! 총 {len(results)}개 종목의 데이터가 {output_filename}에 저장되었습니다.")
    
    # 통계 출력
    if results:
        returns = [r['return_rate'] for r in results]
        avg_return = sum(returns) / len(returns)
        max_return = max(returns)
        min_return = min(returns)
        
        print(f"\n=== 통계 ===")
        print(f"평균 수익률: {avg_return:.2f}%")
        print(f"최고 수익률: {max_return:.2f}%")
        print(f"최저 수익률: {min_return:.2f}%")


if __name__ == "__main__":
    main()
