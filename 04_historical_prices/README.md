# 04. 역사적 가격 데이터 조회

## 설명
특정 종목의 특정 기간 동안의 역사적 가격 데이터를 조회하고 JSON 파일로 저장하는 스크립트입니다.

## 기능
- 지정된 기간 동안의 일별 가격 데이터 조회
- OHLC (시가, 고가, 저가, 종가) 및 거래량 데이터 포함
- JSON 형식으로 결과 저장

## 실행 방법
```bash
python main.py
```

## 기본 설정
- 종목: NVDA (NVIDIA)
- 기간: 2012-01-01 ~ 2012-01-31
- 출력: `{TICKER}_prices_{START_DATE}_{END_DATE}.json`

## 필요한 환경 변수
- `TIINGO_API_KEY`: Tiingo API 키

## 출력 예시
- `NVDA_prices_201211_2012131.json`
