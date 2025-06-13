import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# 이상치 제거 전 데이터 수 출력
print("이상치 제거 전 데이터 수:", len(df))

# 이상치를 제거할 컬럼들
columns_to_clean = ['Price_USD', 'Rating', 'Number_of_Reviews']

# 각 컬럼별로 이상치 제거
for column in columns_to_clean:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"\n{column} 컬럼의 이상치 범위:")
    print(f"하한값: {lower_bound:.2f}")
    print(f"상한값: {upper_bound:.2f}")
    
    # 이상치가 아닌 데이터만 선택
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

print("\n이상치 제거 후 데이터 수:", len(df))

# 이상치 제거 후 데이터 저장
df.to_csv('cosmetics_without_outliers.csv', index=False)
print("\n이상치가 제거된 데이터가 'cosmetics_without_outliers.csv' 파일로 저장되었습니다.")

# 이상치 제거 전후 박스플롯 비교
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('이상치 제거 전후 Box Plot 비교')

# 원본 데이터 박스플롯
original_df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')
for i, column in enumerate(columns_to_clean):
    sns.boxplot(data=original_df[column], ax=axes[0][i])
    axes[0][i].set_title(f'이상치 제거 전 - {column}')
    axes[0][i].tick_params(rotation=45)

# 이상치 제거 후 박스플롯
for i, column in enumerate(columns_to_clean):
    sns.boxplot(data=df[column], ax=axes[1][i])
    axes[1][i].set_title(f'이상치 제거 후 - {column}')
    axes[1][i].tick_params(rotation=45)

plt.tight_layout()
plt.savefig('boxplot_comparison.png')
print("이상치 제거 전후 비교 박스플롯이 'boxplot_comparison.png' 파일로 저장되었습니다.") 