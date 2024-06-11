import pandas as pd

# CSV 파일 읽기
file_path = 'ai-crypto-project-3-live-btc-krw.csv'
df = pd.read_csv(file_path)

# timestamp를 datetime으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# side 값을 기준으로 거래 가치 부호 설정
df['signed_quantity'] = df.apply(lambda row: row['quantity'] if row['side'] == 1 else -row['quantity'], axis=1)

# 거래 가치 계산 (signed_quantity 사용)
df['trade_value'] = df['signed_quantity'] * df['price']

# 수수료 반영
df['net_trade_value'] = df.apply(lambda row: row['trade_value'] + row['fee'] if row['trade_value'] < 0 else row['trade_value'] - row['fee'], axis=1)

# 날짜별 순 거래 가치 합계 계산
daily_value = df.groupby(df['timestamp'].dt.date)['net_trade_value'].sum()

# 일일 PnL 계산
daily_pnl = daily_value.diff().fillna(daily_value)

# 누적 PnL 계산
cumulative_pnl = daily_pnl.cumsum()

# 일일 PnL의 총합 계산 (누적 PnL의 마지막 값)
total_PnL = daily_pnl.sum()

# 최종 PnL 출력
print(f"total PnL (profit minus fee): {total_PnL}")
