import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# 카테고리 빈도수 계산
category_counts = df['Category'].value_counts()

# 그래프 크기 설정
plt.figure(figsize=(15, 8))

# 막대 그래프 생성
sns.barplot(x=category_counts.values, y=category_counts.index)

# 그래프 제목과 레이블 설정
plt.title('화장품 카테고리별 제품 수', fontsize=14, pad=20)
plt.xlabel('제품 수', fontsize=12)
plt.ylabel('카테고리', fontsize=12)

# 각 막대에 값 표시
for i, v in enumerate(category_counts.values):
    plt.text(v, i, f' {v:,}', va='center')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('category_distribution.png', dpi=300, bbox_inches='tight')
print("카테고리 분포 그래프가 'category_distribution.png' 파일로 저장되었습니다.")

# 카테고리별 통계 출력
print("\n=== 카테고리별 제품 수 ===")
for category, count in category_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{category}: {count:,}개 ({percentage:.1f}%)") 