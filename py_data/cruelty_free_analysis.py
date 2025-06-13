import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# 그래프 생성
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1. 파이 차트 - 전체 비율
cruelty_free_counts = df['Cruelty_Free'].value_counts()
colors = ['#ff9999', '#66b3ff']
ax1.pie(cruelty_free_counts, labels=['동물실험 있음', '동물실험 없음'], 
        autopct='%1.1f%%', colors=colors,
        explode=[0.05, 0.05])
ax1.set_title('Cruelty-Free 비율', pad=20)

# 2. 막대 그래프 - 카테고리별 Cruelty-Free 비율
category_cruelty = pd.crosstab(df['Category'], df['Cruelty_Free'], normalize='index') * 100
category_cruelty.plot(kind='bar', stacked=True, ax=ax2, color=colors)
ax2.set_title('카테고리별 Cruelty-Free 비율', pad=20)
ax2.set_xlabel('카테고리')
ax2.set_ylabel('비율 (%)')
ax2.legend(['동물실험 있음', '동물실험 없음'])
plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

# 3. 박스플롯 - Cruelty-Free 여부에 따른 가격 분포
sns.boxplot(data=df, x='Cruelty_Free', y='Price_USD', ax=ax3)
ax3.set_title('Cruelty-Free 여부에 따른 가격 분포', pad=20)
ax3.set_xlabel('Cruelty-Free')
ax3.set_ylabel('가격 (USD)')
ax3.set_xticklabels(['동물실험 있음', '동물실험 없음'])

# 4. 막대 그래프 - 국가별 Cruelty-Free 비율
country_cruelty = pd.crosstab(df['Country_of_Origin'], df['Cruelty_Free'], normalize='index') * 100
country_cruelty.plot(kind='bar', stacked=True, ax=ax4, color=colors)
ax4.set_title('국가별 Cruelty-Free 비율', pad=20)
ax4.set_xlabel('국가')
ax4.set_ylabel('비율 (%)')
ax4.legend(['동물실험 있음', '동물실험 없음'])
plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('cruelty_free_analysis.png', dpi=300, bbox_inches='tight')
print("Cruelty-Free 분석 그래프가 'cruelty_free_analysis.png' 파일로 저장되었습니다.")

# 통계 정보 출력
print("\n=== Cruelty-Free 통계 ===")
total_count = len(df)
cruelty_stats = df['Cruelty_Free'].value_counts()
print("\n1. 전체 비율:")
for status, count in cruelty_stats.items():
    percentage = (count / total_count) * 100
    print(f"- {'동물실험 없음' if status else '동물실험 있음'}: {count:,}개 ({percentage:.1f}%)")

print("\n2. 카테고리별 Cruelty-Free 비율:")
category_stats = pd.crosstab(df['Category'], df['Cruelty_Free'])
for category in category_stats.index:
    total = category_stats.loc[category].sum()
    cruelty_free_count = category_stats.loc[category, True]
    percentage = (cruelty_free_count / total) * 100
    print(f"\n{category}:")
    print(f"- 총 제품 수: {total:,}개")
    print(f"- 동물실험 없는 제품: {cruelty_free_count:,}개 ({percentage:.1f}%)")

print("\n3. 가격 통계:")
price_stats = df.groupby('Cruelty_Free')['Price_USD'].agg(['mean', 'median', 'std']).round(2)
for status, stats in price_stats.iterrows():
    print(f"\n{'동물실험 없음' if status else '동물실험 있음'}:")
    print(f"- 평균 가격: ${stats['mean']:,.2f}")
    print(f"- 중간 가격: ${stats['median']:,.2f}")
    print(f"- 표준편차: ${stats['std']:,.2f}")

print("\n4. 국가별 Cruelty-Free 비율 TOP 5:")
country_stats = pd.crosstab(df['Country_of_Origin'], df['Cruelty_Free'])
country_stats['비율'] = (country_stats[True] / (country_stats[True] + country_stats[False]) * 100).round(1)
print(country_stats.nlargest(5, '비율')[['비율']].to_string()) 