# 05. 연간 수익률(YoY) 계산

## 설명
여러 종목의 1년 전 대비 수익률(Year-over-Year Return)을 계산하고 CSV 파일로 저장하는 스크립트입니다.

## 기능
- 개별 종목 또는 다수 종목의 YoY 수익률 계산
- S&P 500 전체 종목 분석 지원
- 통계 정보 제공 (평균, 최고, 최저 수익률)
- CSV 파일로 결과 저장

## 실행 방법

### 기본 실행 (S&P 500 전체 종목)
```bash
python main.py
```

### 특정 종목 지정
```bash
python main.py -t AAPL MSFT GOOGL
```

### 파일에서 종목 읽기
```bash
python main.py -f my_tickers.txt
```

### 특정 날짜 기준으로 조회
```bash
python main.py -d 2025-12-31
```

## 옵션
- `-t, --tickers`: 비교할 티커 리스트 (공백으로 구분)
- `-f, --file`: 티커 리스트 파일 경로
- `-d, --date`: 비교 기준 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)

## 출력 파일
- `price_comparison_YYYYMMDD_YYYYMMDD.csv`: 수익률 비교 결과

## 필요한 환경 변수
- `TIINGO_API_KEY`: Tiingo API 키

## 출력 정보
- 종목명
- 1년 전 가격
- 현재 가격
- 수익률 (%)
- 통계 (평균, 최고, 최저 수익률)
