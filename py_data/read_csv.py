import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# 데이터프레임의 처음 5행 출력
print("\n처음 5행:")
print(df.head())

# 데이터프레임의 기본 정보 출력
print("\n데이터프레임 정보:")
print(df.info()) 