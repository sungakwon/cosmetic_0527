import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
original_df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')
cleaned_df = pd.read_csv('cosmetics_without_outliers.csv')

# 분석할 컬럼들
columns_to_analyze = ['Price_USD', 'Rating', 'Number_of_Reviews']

# 서브플롯 생성
fig, axes = plt.subplots(2, 3, figsize=(20, 10))
fig.suptitle('이상치 제거 전후 Box Plot 비교', fontsize=16, y=1.02)

# 각 컬럼별로 박스플롯 생성
for i, column in enumerate(columns_to_analyze):
    # 이상치 제거 전 박스플롯
    sns.boxplot(data=original_df[column], ax=axes[0][i])
    axes[0][i].set_title(f'이상치 제거 전 - {column}')
    axes[0][i].tick_params(rotation=45)
    
    # 이상치 제거 후 박스플롯
    sns.boxplot(data=cleaned_df[column], ax=axes[1][i])
    axes[1][i].set_title(f'이상치 제거 후 - {column}')
    axes[1][i].tick_params(rotation=45)

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('boxplot_comparison.png', dpi=300, bbox_inches='tight')
print("박스플롯이 'boxplot_comparison.png' 파일로 저장되었습니다.")

# 기본 통계 정보 출력
for column in columns_to_analyze:
    print(f"\n=== {column} 통계 ===")
    print("\n이상치 제거 전:")
    print(original_df[column].describe().round(2))
    print("\n이상치 제거 후:")
    print(cleaned_df[column].describe().round(2)) 