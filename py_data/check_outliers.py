import pandas as pd
import numpy as np

# 원본 데이터와 이상치가 제거된 데이터 읽기
original_df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')
cleaned_df = pd.read_csv('cosmetics_without_outliers.csv')

# 분석할 컬럼들
columns_to_analyze = ['Price_USD', 'Rating', 'Number_of_Reviews']

print("=== 이상치 제거 분석 결과 ===")
print(f"\n전체 데이터 수:")
print(f"원본 데이터: {len(original_df):,}개")
print(f"이상치 제거 후: {len(cleaned_df):,}개")
print(f"제거된 데이터 수: {len(original_df) - len(cleaned_df):,}개")

for column in columns_to_analyze:
    print(f"\n=== {column} 컬럼 분석 ===")
    
    # 원본 데이터의 사분위수 계산
    Q1 = original_df[column].quantile(0.25)
    Q3 = original_df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # 이상치 개수 계산
    outliers = original_df[(original_df[column] < lower_bound) | (original_df[column] > upper_bound)]
    outliers_count = len(outliers)
    
    print(f"\n이상치 범위:")
    print(f"하한값: {lower_bound:.2f}")
    print(f"상한값: {upper_bound:.2f}")
    
    print(f"\n이상치 수: {outliers_count:,}개")
    
    print(f"\n최대값 비교:")
    print(f"원본 데이터 최대값: {original_df[column].max():,.2f}")
    print(f"이상치 제거 후 최대값: {cleaned_df[column].max():,.2f}")
    
    print(f"\n기술 통계량:")
    print("원본 데이터:")
    print(original_df[column].describe().round(2))
    print("\n이상치 제거 후:")
    print(cleaned_df[column].describe().round(2)) 