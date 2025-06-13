import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# 그래프 생성을 위한 figure 설정
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1. 파이 차트 - 전체 피부 타입 분포
skin_type_counts = df['Skin_Type'].value_counts()
colors = sns.color_palette('pastel')
ax1.pie(skin_type_counts, labels=skin_type_counts.index, 
        autopct='%1.1f%%', colors=colors,
        explode=[0.05] * len(skin_type_counts))
ax1.set_title('피부 타입 분포', pad=20)

# 2. 막대 그래프 - 피부 타입별 제품 수
sns.barplot(x=skin_type_counts.index, y=skin_type_counts.values, 
           palette='pastel', ax=ax2)
ax2.set_title('피부 타입별 제품 수', pad=20)
ax2.set_xlabel('피부 타입')
ax2.set_ylabel('제품 수')
plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

# 각 막대 위에 값 표시
for i, v in enumerate(skin_type_counts.values):
    ax2.text(i, v, str(v), ha='center', va='bottom')

# 3. 카테고리별 피부 타입 분포
category_skin_type = pd.crosstab(df['Category'], df['Skin_Type'], normalize='index') * 100
category_skin_type.plot(kind='bar', stacked=True, ax=ax3, 
                       colormap='Pastel1')
ax3.set_title('카테고리별 피부 타입 분포', pad=20)
ax3.set_xlabel('카테고리')
ax3.set_ylabel('비율 (%)')
plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
ax3.legend(title='피부 타입', bbox_to_anchor=(1.05, 1), loc='upper left')

# 4. 피부 타입별 평균 가격
avg_price_by_skin_type = df.groupby('Skin_Type')['Price_USD'].mean().sort_values(ascending=False)
sns.barplot(x=avg_price_by_skin_type.index, y=avg_price_by_skin_type.values, 
           palette='pastel', ax=ax4)
ax4.set_title('피부 타입별 평균 가격', pad=20)
ax4.set_xlabel('피부 타입')
ax4.set_ylabel('평균 가격 (USD)')
plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')

# 각 막대 위에 값 표시
for i, v in enumerate(avg_price_by_skin_type.values):
    ax4.text(i, v, f'${v:.2f}', ha='center', va='bottom')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('skin_type_analysis.png', dpi=300, bbox_inches='tight')
print("피부 타입 분석 그래프가 'skin_type_analysis.png' 파일로 저장되었습니다.")

# 통계 정보 출력
print("\n=== 피부 타입 통계 ===")
print("\n1. 피부 타입별 제품 수:")
for skin_type, count in skin_type_counts.items():
    percentage = (count / len(df)) * 100
    print(f"- {skin_type}: {count:,}개 ({percentage:.1f}%)")

print("\n2. 카테고리별 주요 피부 타입:")
for category in df['Category'].unique():
    category_data = df[df['Category'] == category]['Skin_Type'].value_counts()
    top_skin_type = category_data.index[0]
    percentage = (category_data[top_skin_type] / category_data.sum()) * 100
    print(f"\n{category}:")
    print(f"- 가장 많은 피부 타입: {top_skin_type} ({percentage:.1f}%)")
    print(f"- 총 제품 수: {category_data.sum():,}개")

print("\n3. 피부 타입별 가격 통계:")
price_stats = df.groupby('Skin_Type')['Price_USD'].agg(['mean', 'median', 'std', 'count']).round(2)
price_stats = price_stats.sort_values('count', ascending=False)
for skin_type, stats in price_stats.iterrows():
    print(f"\n{skin_type}:")
    print(f"- 제품 수: {stats['count']:,}개")
    print(f"- 평균 가격: ${stats['mean']:,.2f}")
    print(f"- 중간 가격: ${stats['median']:,.2f}")
    print(f"- 표준편차: ${stats['std']:,.2f}") 