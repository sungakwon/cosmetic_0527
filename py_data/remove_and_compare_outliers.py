import pandas as pd
import numpy as np

# 데이터 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')
print("=== 이상치 제거 분석 결과 ===")
print(f"원본 데이터 수: {len(df):,}개\n")

# 이상치를 제거할 컬럼들
columns_to_clean = ['Price_USD', 'Rating', 'Number_of_Reviews']

# 원본 데이터의 통계량 저장
original_stats = {
    'count': len(df),
    'means': {col: df[col].mean() for col in columns_to_clean},
    'maxes': {col: df[col].max() for col in columns_to_clean}
}

# 각 컬럼별로 이상치 제거
for column in columns_to_clean:
    print(f"\n=== {column} 컬럼 분석 ===")
    
    # 사분위수 계산
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # 이상치가 아닌 데이터만 선택
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    # 이상치 수 계산
    outliers_count = original_stats['count'] - len(df)
    
    print(f"\n1. 데이터 수 비교")
    print(f"- 이상치 제거 전: {original_stats['count']:,}개")
    print(f"- 이상치 제거 후: {len(df):,}개")
    print(f"- 제거된 이상치: {outliers_count:,}개 ({(outliers_count/original_stats['count']*100):.1f}%)")
    
    print(f"\n2. 평균값 비교")
    print(f"- 이상치 제거 전: {original_stats['means'][column]:,.2f}")
    print(f"- 이상치 제거 후: {df[column].mean():,.2f}")
    
    print(f"\n3. 최대값 비교")
    print(f"- 이상치 제거 전: {original_stats['maxes'][column]:,.2f}")
    print(f"- 이상치 제거 후: {df[column].max():,.2f}")

print(f"\n=== 최종 결과 ===")
print(f"모든 컬럼의 이상치 제거 후 남은 데이터 수: {len(df):,}개")
print(f"총 제거된 데이터 수: {original_stats['count'] - len(df):,}개")

# 이상치가 제거된 데이터 저장
df.to_csv('cosmetics_without_outliers.csv', index=False)
print("\n이상치가 제거된 데이터를 'cosmetics_without_outliers.csv' 파일로 저장했습니다.") 