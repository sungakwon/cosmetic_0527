import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# Rating 등급 설정 (1점대, 2점대, 3점대, 4점대, 5점대)
df['Rating_Grade'] = pd.cut(df['Rating'], 
                          bins=[0, 1.99, 2.99, 3.99, 4.99, 5.0],
                          labels=['1점대', '2점대', '3점대', '4점대', '5점대'])

# 그래프 생성
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1. 박스플롯 - 등급별 리뷰 수 분포
sns.boxplot(data=df, x='Rating_Grade', y='Number_of_Reviews', ax=ax1)
ax1.set_title('평점 등급별 리뷰 수 분포', pad=20)
ax1.set_xlabel('평점 등급')
ax1.set_ylabel('리뷰 수')

# 2. 바이올린 플롯 - 등급별 리뷰 수 분포 (밀도 포함)
sns.violinplot(data=df, x='Rating_Grade', y='Number_of_Reviews', ax=ax2)
ax2.set_title('평점 등급별 리뷰 수 분포 (밀도 포함)', pad=20)
ax2.set_xlabel('평점 등급')
ax2.set_ylabel('리뷰 수')

# 3. 산점도 - Rating과 리뷰 수의 관계
sns.scatterplot(data=df, x='Rating', y='Number_of_Reviews', alpha=0.5, ax=ax3)
ax3.set_title('평점과 리뷰 수의 관계', pad=20)
ax3.set_xlabel('평점')
ax3.set_ylabel('리뷰 수')

# 4. 막대 그래프 - 등급별 평균 리뷰 수
avg_reviews = df.groupby('Rating_Grade')['Number_of_Reviews'].agg(['mean', 'count'])
ax4.bar(avg_reviews.index, avg_reviews['mean'])
ax4.set_title('평점 등급별 평균 리뷰 수', pad=20)
ax4.set_xlabel('평점 등급')
ax4.set_ylabel('평균 리뷰 수')

# 막대 위에 값 표시
for i, v in enumerate(avg_reviews['mean']):
    ax4.text(i, v, f'평균: {v:,.0f}\n제품수: {avg_reviews["count"][i]:,}개', 
             ha='center', va='bottom')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('rating_grade_analysis.png', dpi=300, bbox_inches='tight')
print("평점 등급별 분석 그래프가 'rating_grade_analysis.png' 파일로 저장되었습니다.")

# 통계 정보 출력
print("\n=== 평점 등급별 리뷰 통계 ===")
stats = df.groupby('Rating_Grade').agg({
    'Number_of_Reviews': ['count', 'mean', 'std', 'min', 'max'],
    'Rating': ['mean', 'min', 'max']
}).round(2)

for grade in stats.index:
    grade_stats = stats.loc[grade]
    print(f"\n{grade}:")
    print(f"- 제품 수: {grade_stats['Number_of_Reviews']['count']:,}개")
    print(f"- 평균 리뷰 수: {grade_stats['Number_of_Reviews']['mean']:,.2f} "
          f"(표준편차: {grade_stats['Number_of_Reviews']['std']:,.2f})")
    print(f"- 리뷰 수 범위: {grade_stats['Number_of_Reviews']['min']:,} ~ "
          f"{grade_stats['Number_of_Reviews']['max']:,}")
    print(f"- 평균 평점: {grade_stats['Rating']['mean']:.2f} "
          f"(범위: {grade_stats['Rating']['min']} ~ {grade_stats['Rating']['max']})")

# 상관관계 계산
correlation = df['Rating'].corr(df['Number_of_Reviews'])
print(f"\n평점과 리뷰 수의 상관계수: {correlation:.4f}")

# 각 등급별 최다 리뷰 제품
print("\n=== 평점 등급별 최다 리뷰 제품 TOP 3 ===")
for grade in df['Rating_Grade'].unique():
    grade_data = df[df['Rating_Grade'] == grade].nlargest(3, 'Number_of_Reviews')
    print(f"\n{grade} TOP 3:")
    for _, product in grade_data.iterrows():
        print(f"- {product['Product_Name']}: {product['Number_of_Reviews']:,}개 리뷰 "
              f"(평점: {product['Rating']:.1f})") 