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

# Design tokens from Pencil guide
BG_COLOR = '#0B0B0C'
SURFACE_COLOR = '#131316'
SURFACE_2_COLOR = '#18181C'
BORDER_COLOR = '#26262B'
BORDER_BRIGHT_COLOR = '#36363E'
TEXT_COLOR = '#EDEDEF'
MUTED_COLOR = '#9B9BA3'
ACCENT_CYAN = '#22D3EE'
ACCENT_CRIMSON = '#FF4D5E'

# Set up matplotlib figure
fig = plt.figure(figsize=(10.8, 7.8), facecolor=SURFACE_COLOR)
ax = plt.axes()
ax.set_facecolor(SURFACE_COLOR)

# Classify and split for color coding
df_alternative = df_cp_result[df_cp_result['상권 분류'] == '대안 상권 (숨은 꿀역)']
df_saturated = df_cp_result[df_cp_result['상권 분류'] == '과포화 상권 (기존 핫플)']

# Plot scatter points
plt.scatter(
    df_alternative['하차인구(Cost)'],
    df_alternative['상가수(Benefit)'],
    color=ACCENT_CYAN,
    s=220,
    alpha=0.9,
    edgecolor='#000000',
    linewidth=1.2,
    label='대안 상권 (숨은 꿀역)'
)
plt.scatter(
    df_saturated['하차인구(Cost)'],
    df_saturated['상가수(Benefit)'],
    color=ACCENT_CRIMSON,
    s=220,
    alpha=0.9,
    edgecolor='#000000',
    linewidth=1.2,
    label='과포화 상권 (기존 핫플)'
)

# Axis labels
plt.xlabel("대중교통 하차 인구 총량 (Cost) [단위: 천 명]", fontsize=13, fontweight='bold', color=TEXT_COLOR, labelpad=12)
plt.ylabel("반경 500m 내 상가 수 (Benefit) [단위: 개]", fontsize=13, fontweight='bold', color=TEXT_COLOR, labelpad=12)

# Set borders/spines colors
for spine in ax.spines.values():
    spine.set_color(BORDER_COLOR)
    spine.set_linewidth(1.5)

# Ticks settings
ax.tick_params(colors=MUTED_COLOR, which='both', labelsize=11)

# Grid settings
plt.grid(True, linestyle=":", alpha=0.3, color=MUTED_COLOR)

# Label points
for i in range(len(df_cp_result)):
    x_offset = 35
    y_offset = 2
    
    station = df_cp_result["지하철역"][i]
    if station == '상수':
        y_offset = 12
        x_offset = -60
    elif station == '송파나루':
        y_offset = -20
        x_offset = -15
    elif station == '압구정':
        y_offset = -20
        x_offset = -15
    elif station == '명동':
        y_offset = 12
        x_offset = -30
    elif station == '건대입구':
        y_offset = -20
        x_offset = -30
    elif station == '성수':
        y_offset = 12
        x_offset = -35
    elif station == '망원':
        y_offset = 10
        x_offset = -30
    elif station == '이태원':
        y_offset = -18
        x_offset = 15
        
    plt.text(
        df_cp_result["하차인구(Cost)"][i] + x_offset,
        df_cp_result["상가수(Benefit)"][i] + y_offset,
        df_cp_result["지하철역"][i],
        fontsize=12,
        fontweight="bold",
        color=TEXT_COLOR
    )

# Target Zone Box
plt.text(
    1500,
    220,
    "★ Target Zone\n인파는 적고\n선택지는 풍부함",
    color=ACCENT_CYAN,
    fontweight="bold",
    fontsize=13,
    bbox=dict(facecolor=SURFACE_2_COLOR, alpha=0.85, edgecolor=ACCENT_CYAN, boxstyle="round,pad=0.6"),
)

# Divider lines
plt.axvline(x=1500, color=BORDER_BRIGHT_COLOR, linestyle='--', linewidth=1.5, alpha=0.7)
plt.axhline(y=220, color=BORDER_BRIGHT_COLOR, linestyle='--', linewidth=1.5, alpha=0.7)

# Legend settings
leg = plt.legend(title="상권 분류", title_fontsize="12", loc="lower right", fontsize="11", facecolor=SURFACE_2_COLOR, edgecolor=BORDER_COLOR)
leg.get_title().set_color(TEXT_COLOR)
for text in leg.get_texts():
    text.set_color(TEXT_COLOR)

plt.tight_layout()

# Save plot
os.makedirs('발표자료', exist_ok=True)
plt.savefig('발표자료/cp_matrix_dark.png', dpi=200, facecolor=SURFACE_COLOR, edgecolor='none')
plt.close()
print("Dark plot successfully saved to 발표자료/cp_matrix_dark.png")
