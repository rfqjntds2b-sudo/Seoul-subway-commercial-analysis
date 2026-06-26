import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set Korean Font for Matplotlib on Windows
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# Load data
df = pd.read_csv('subway_bus_shop_merged_result_optimized.csv', encoding='utf-8-sig')

# Define target stations
target_stations = ['상수', '송파나루', '석촌고분', '망원', '이태원', '강남', '홍대입구', '성수', '신촌', '여의도', '명동', '건대입구', '압구정']

df_cp_result = df[df['정제역명'].isin(target_stations)].copy()
df_cp_result = df_cp_result.rename(columns={
    '정제역명': '지하철역',
    '총_유입_인구': '하차인구(Cost)',
    '주변_상가_수': '상가수(Benefit)'
})

# Scale down Cost by 1000
df_cp_result['하차인구(Cost)'] = df_cp_result['하차인구(Cost)'] / 1000
df_cp_result = df_cp_result.reset_index(drop=True)

# Classify stations for the legend
df_cp_result['상권 분류'] = np.where(df_cp_result['하차인구(Cost)'] < 1500, '대안 상권 (숨은 꿀역)', '과포화 상권 (기존 핫플)')

# Plot
plt.figure(figsize=(10, 8))

# Classify and split for color coding
df_alternative = df_cp_result[df_cp_result['상권 분류'] == '대안 상권 (숨은 꿀역)']
df_saturated = df_cp_result[df_cp_result['상권 분류'] == '과포화 상권 (기존 핫플)']

# Plot scatter points using native matplotlib
plt.scatter(
    df_alternative['하차인구(Cost)'],
    df_alternative['상가수(Benefit)'],
    color='#1F77B4',
    s=180,
    alpha=0.9,
    edgecolor='black',
    linewidth=1.2,
    label='대안 상권 (숨은 꿀역)'
)
plt.scatter(
    df_saturated['하차인구(Cost)'],
    df_saturated['상가수(Benefit)'],
    color='#FF7F0E',
    s=180,
    alpha=0.9,
    edgecolor='black',
    linewidth=1.2,
    label='과포화 상권 (기존 핫플)'
)

# 타이틀 및 축 레이블 설정 (두괄식 메시지 반영)
plt.title(
    "③ 공간 스캔 기반 혼잡 가성비(C/P) 매트릭스\n[결론: Low Cost / High Benefit 대안 상권 도출]",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
plt.xlabel("대중교통 하차 인구 총량 (Cost) [단위: 천 명]", fontsize=12, labelpad=10)
plt.ylabel("반경 500m 내 상가 수 (Benefit) [단위: 개]", fontsize=12, labelpad=10)

# 각 데이터 포인트(역 이름) 라벨링 생성
for i in range(len(df_cp_result)):
    # Default label offsets
    x_offset = 30
    y_offset = 2
    
    # Adjust position slightly to prevent overlaps
    station = df_cp_result["지하철역"][i]
    if station == '상수':
        y_offset = 10
        x_offset = -60
    elif station == '송파나루':
        y_offset = -18
        x_offset = -15
    elif station == '압구정':
        y_offset = -18
        x_offset = -15
    elif station == '명동':
        y_offset = 10
        x_offset = -30
    elif station == '건대입구':
        y_offset = -18
        x_offset = -30
    elif station == '성수':
        y_offset = 10
        x_offset = -35
    elif station == '망원':
        y_offset = 8
        x_offset = -30
    elif station == '이태원':
        y_offset = -15
        x_offset = 15
        
    plt.text(
        df_cp_result["하차인구(Cost)"][i] + x_offset,
        df_cp_result["상가수(Benefit)"][i] + y_offset,
        df_cp_result["지하철역"][i],
        fontsize=11,
        fontweight="bold",
    )

# 2사분면(우수 영역) 강조 텍스트 박스
plt.text(
    1500,
    220,
    "★ Target Zone\n인파는 적고\n선택지는 풍부함",
    color="#1F77B4",
    fontweight="bold",
    fontsize=12,
    bbox=dict(facecolor="#E6F2FF", alpha=0.8, edgecolor="#1F77B4", boxstyle="round,pad=0.5"),
)

# Divider at Cost = 1500 (horizontal boundary) and Benefit = 220 (vertical boundary)
plt.axvline(x=1500, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=220, color='gray', linestyle='--', alpha=0.5)

plt.legend(title="상권 분류", title_fontsize="11", loc="lower right", fontsize="10")
plt.grid(True, linestyle=":", alpha=0.4)
plt.tight_layout()

# Save plot
os.makedirs('발표자료', exist_ok=True)
plt.savefig('발표자료/cp_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("Plot successfully saved to 발표자료/cp_matrix.png")
