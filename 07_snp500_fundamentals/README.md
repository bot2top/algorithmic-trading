# S&P 500 Fundamentals (2025 Q0)

S&P 500 종목 중 2025년 0분기(연간 데이터) fundamental 데이터를 수집합니다.

## 실행 방법

```bash
conda activate altr
python main.py
```

## 데이터 소스

- **S&P 500 티커 리스트**: Wikipedia
- **Fundamental 데이터**: Tiingo API

## 출력 파일

- `data/snp500_fundamentals_2025Q0_{timestamp}.csv` - CSV 형식의 fundamental 데이터
- `data/snp500_fundamentals_2025Q0_{timestamp}.json` - JSON 형식의 원본 데이터
- `data/tickers_with_2025Q0_{timestamp}.txt` - 데이터가 존재하는 티커 목록

## 포함 데이터

- Balance Sheet (대차대조표)
- Income Statement (손익계산서)
- Cash Flow Statement (현금흐름표)
- Overview (개요 지표: ROA, ROE, EPS 등)
