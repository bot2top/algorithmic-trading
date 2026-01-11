# 03. S&P 500 종목 리스트 크롤링

## 설명
위키피디아에서 S&P 500 종목 리스트를 크롤링하여 저장하는 스크립트입니다.

## 기능
- Wikipedia에서 S&P 500 종목 리스트 수집
- 티커 심볼을 텍스트 파일로 저장
- 날짜별 파일명 생성 (`snp500_tickers_YYYYMMDD.txt`)

## 실행 방법
```bash
python main.py
```

## 출력 파일
- `snp500_tickers_YYYYMMDD.txt`: 수집된 티커 리스트 (한 줄에 하나씩)

## 의존성
- pandas
- requests
