import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# 카테고리 그룹 매핑 정의
category_groups = {
    '스킨케어': ['Face Moisturizer', 'Face Serum', 'Face Wash', 'Face Mask', 'Eye Care', 'Toner', 
                'Face Oil', 'Face Scrub & Exfoliator', 'Sunscreen', 'Lip Care'],
    '메이크업': ['Foundation', 'Concealer', 'Face Powder', 'Blush', 'Bronzer & Contour', 
               'Highlighter', 'Eyeshadow', 'Eyeliner', 'Mascara', 'Eyebrow', 'Lip Color', 
               'Makeup Remover', 'Primer', 'Setting Spray', 'Lipstick', 'Lip Gloss', 'Lip Liner'],
    '헤어케어': ['Shampoo', 'Conditioner', 'Hair Treatment', 'Hair Styling', 'Hair Color'],
    '바디케어': ['Body Lotion & Oil', 'Body Wash', 'Hand Care', 'Deodorant', 'Feminine Care']
}

# 카테고리 그룹 컬럼 생성
def get_category_group(category):
    for group, categories in category_groups.items():
        if category in categories:
            return group
    return '기타'

df['Category_Group'] = df['Category'].apply(get_category_group)

# 4가지 주요 카테고리만 선택
main_categories = ['헤어케어', '바디케어', '스킨케어', '메이크업']
df_main = df[df['Category_Group'].isin(main_categories)]

# Usage_Frequency를 순서가 있는 카테고리로 변환
frequency_order = ['Daily', 'Weekly', 'Monthly', 'Occasional']
df_main['Usage_Frequency'] = pd.Categorical(df_main['Usage_Frequency'], categories=frequency_order, ordered=True)

# 그래프 생성
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

# 1. 스택 바 차트 - 카테고리별 사용 빈도 비율
freq_by_category = pd.crosstab(df_main['Category_Group'], df_main['Usage_Frequency'], normalize='index') * 100
freq_by_category.plot(kind='bar', stacked=True, ax=ax1)
ax1.set_title('카테고리별 사용 빈도 분포', pad=20)
ax1.set_xlabel('카테고리')
ax1.set_ylabel('비율 (%)')
ax1.legend(title='사용 빈도', bbox_to_anchor=(1.05, 1))
ax1.tick_params(axis='x', rotation=45)

# 2. 히트맵 - 카테고리별 사용 빈도 수
freq_counts = pd.crosstab(df_main['Category_Group'], df_main['Usage_Frequency'])
sns.heatmap(freq_counts, annot=True, fmt='d', cmap='YlOrRd', ax=ax2)
ax2.set_title('카테고리별 사용 빈도 히트맵')
ax2.set_xlabel('사용 빈도')
ax2.set_ylabel('카테고리')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('usage_frequency_4categories.png', dpi=300, bbox_inches='tight')
print("사용 빈도 분포 그래프가 'usage_frequency_4categories.png' 파일로 저장되었습니다.")

# 상세 통계 출력
print("\n=== 카테고리별 사용 빈도 통계 ===")
for category in main_categories:
    category_data = df_main[df_main['Category_Group'] == category]
    freq_counts = category_data['Usage_Frequency'].value_counts()
    total = len(category_data)
    
    print(f"\n{category} (총 {total:,}개 제품):")
    for freq in frequency_order:
        count = freq_counts.get(freq, 0)
        percentage = (count / total) * 100
        print(f"- {freq}: {count:,}개 ({percentage:.1f}%)")

# 카테고리별 가장 많이 사용되는 제품 TOP 3
print("\n=== 카테고리별 Daily 사용 제품 TOP 3 ===")
for category in main_categories:
    daily_products = df_main[(df_main['Category_Group'] == category) & 
                            (df_main['Usage_Frequency'] == 'Daily')].nlargest(3, 'Rating')
    print(f"\n{category} TOP 3 Daily 사용 제품:")
    for _, product in daily_products.iterrows():
        print(f"- {product['Product_Name']} (평점: {product['Rating']:.1f})") 