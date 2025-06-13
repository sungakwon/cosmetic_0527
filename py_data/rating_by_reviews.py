import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# 리뷰 개수 구간 설정
df['Review_Range'] = pd.qcut(df['Number_of_Reviews'], q=5, labels=['매우 적음', '적음', '보통', '많음', '매우 많음'])

# 그래프 생성
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

# 1. 산점도 - 리뷰 개수와 평점의 관계
sns.scatterplot(data=df, x='Number_of_Reviews', y='Rating', alpha=0.5, ax=ax1)
ax1.set_title('리뷰 개수와 평점의 관계', pad=20)
ax1.set_xlabel('리뷰 개수')
ax1.set_ylabel('평점')

# 추세선 추가
z = np.polyfit(df['Number_of_Reviews'], df['Rating'], 1)
p = np.poly1d(z)
ax1.plot(df['Number_of_Reviews'], p(df['Number_of_Reviews']), "r--", alpha=0.8, 
         label=f'추세선 (기울기: {z[0]:.4f})')
ax1.legend()

# 2. 박스플롯 - 리뷰 개수 구간별 평점 분포
sns.boxplot(data=df, x='Review_Range', y='Rating', ax=ax2)
ax2.set_title('리뷰 개수 구간별 평점 분포', pad=20)
ax2.set_xlabel('리뷰 개수 구간')
ax2.set_ylabel('평점')

# 3. 바이올린 플롯 - 리뷰 개수 구간별 평점 분포 (밀도 포함)
sns.violinplot(data=df, x='Review_Range', y='Rating', ax=ax3)
ax3.set_title('리뷰 개수 구간별 평점 분포 (밀도 포함)', pad=20)
ax3.set_xlabel('리뷰 개수 구간')
ax3.set_ylabel('평점')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('rating_by_reviews.png', dpi=300, bbox_inches='tight')
print("리뷰 개수와 평점 관계 그래프가 'rating_by_reviews.png' 파일로 저장되었습니다.")

# 통계 정보 출력
print("\n=== 리뷰 개수 구간별 평점 통계 ===")
stats = df.groupby('Review_Range').agg({
    'Rating': ['count', 'mean', 'std', 'min', 'max'],
    'Number_of_Reviews': ['min', 'max']
}).round(2)

for range_name in stats.index:
    range_stats = stats.loc[range_name]
    print(f"\n{range_name}:")
    print(f"- 제품 수: {range_stats['Rating']['count']:,}개")
    print(f"- 평균 평점: {range_stats['Rating']['mean']:.2f} (표준편차: {range_stats['Rating']['std']:.2f})")
    print(f"- 평점 범위: {range_stats['Rating']['min']} ~ {range_stats['Rating']['max']}")
    print(f"- 리뷰 개수 범위: {range_stats['Number_of_Reviews']['min']:,} ~ {range_stats['Number_of_Reviews']['max']:,}")

# 상관관계 계산
correlation = df['Number_of_Reviews'].corr(df['Rating'])
print(f"\n리뷰 개수와 평점의 상관계수: {correlation:.4f}")

# 리뷰 개수 구간별 상위 평점 제품
print("\n=== 리뷰 개수 구간별 최고 평점 제품 TOP 3 ===")
for range_name in df['Review_Range'].unique():
    range_data = df[df['Review_Range'] == range_name].nlargest(3, 'Rating')
    print(f"\n{range_name} 구간 TOP 3:")
    for _, product in range_data.iterrows():
        print(f"- {product['Product_Name']}: 평점 {product['Rating']:.1f} "
              f"(리뷰 {product['Number_of_Reviews']:,}개)") 