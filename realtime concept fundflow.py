import akshare as ak
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 获取实时概念资金流数据
stock_fund_flow_concept_df = ak.stock_fund_flow_concept(symbol="即时")

# 排序数据框按净额的绝对值
sorted_df = stock_fund_flow_concept_df.iloc[(-stock_fund_flow_concept_df['净额'].abs()).argsort()]

# 选择前五十个概念
top_fifty_concepts = sorted_df.head(50)

# 绘制图表
plt.figure(figsize=(12, 10))
# 绘制前五十个概念的水平柱状图
bars = plt.barh(top_fifty_concepts['行业'], top_fifty_concepts['净额'], color=['red' if value > 0 else 'green' for value in top_fifty_concepts['净额']])
plt.xlabel('净额（亿元）')
plt.ylabel('概念')
plt.title('前五十个概念 - 即时概念资金流')

for i, value in enumerate(top_fifty_concepts['净额']):
    # 将标注放在柱状图的左侧
    plt.text(value, i, f"{top_fifty_concepts.iloc[i]['行业-涨跌幅']}%", va='center', ha='left' if value > 0 else 'right', color='black')

plt.tight_layout()
plt.show()