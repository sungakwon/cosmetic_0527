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
               'Makeup Remover', 'Primer', 'Setting Spray'],
    '헤어케어': ['Shampoo', 'Conditioner', 'Hair Treatment', 'Hair Styling', 'Hair Color'],
    '향수': ['Perfume'],
    '개인 관리': ['Body Lotion & Oil', 'Body Wash', 'Hand Care', 'Deodorant', 'Feminine Care']
}

# 카테고리 그룹 컬럼 생성
def get_category_group(category):
    for group, categories in category_groups.items():
        if category in categories:
            return group
    return '기타'

df['Category_Group'] = df['Category'].apply(get_category_group)

# Usage_Frequency를 순서가 있는 카테고리로 변환
frequency_order = ['Daily', 'Weekly', 'Monthly', 'Occasional']
df['Usage_Frequency'] = pd.Categorical(df['Usage_Frequency'], categories=frequency_order, ordered=True)

# 그래프 생성
plt.figure(figsize=(15, 8))

# 카테고리별 Usage_Frequency 분포를 보여주는 stacked bar plot 생성
freq_by_category = pd.crosstab(df['Category_Group'], df['Usage_Frequency'], normalize='index') * 100
freq_by_category.plot(kind='bar', stacked=True)

# 그래프 스타일링
plt.title('카테고리 그룹별 사용 빈도 분포', fontsize=14, pad=20)
plt.xlabel('카테고리 그룹', fontsize=12)
plt.ylabel('비율 (%)', fontsize=12)
plt.legend(title='사용 빈도', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('usage_frequency_distribution.png', dpi=300, bbox_inches='tight')
print("사용 빈도 분포 그래프가 'usage_frequency_distribution.png' 파일로 저장되었습니다.")

# 상세 통계 출력
print("\n=== 카테고리 그룹별 사용 빈도 통계 ===")
for group in df['Category_Group'].unique():
    group_data = df[df['Category_Group'] == group]
    freq_counts = group_data['Usage_Frequency'].value_counts()
    total = len(group_data)
    
    print(f"\n{group} (총 {total:,}개 제품):")
    for freq in frequency_order:
        count = freq_counts.get(freq, 0)
        percentage = (count / total) * 100
        print(f"- {freq}: {count:,}개 ({percentage:.1f}%)") 