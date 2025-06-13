import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 읽기
df = pd.read_csv('most_used_beauty_cosmetics_products_extended.csv')

# figure 크기 설정
plt.figure(figsize=(15, 8))

# 수치형 데이터 컬럼들에 대해 박스플롯 생성
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
sns.boxplot(data=df[numeric_columns])

# x축 레이블 회전
plt.xticks(rotation=45, ha='right')

# 제목 설정
plt.title('수치형 데이터의 Box Plot')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('boxplot_analysis.png')
print("박스플롯이 'boxplot_analysis.png' 파일로 저장되었습니다.") 