import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 获取数据
stock_individual_fund_flow_rank_df = ak.stock_individual_fund_flow_rank(indicator="今日")

# 将 "-" 替换为 0，并将列转换为数字类型
stock_individual_fund_flow_rank_df["今日主力净流入-净额"] = stock_individual_fund_flow_rank_df["今日主力净流入-净额"].replace("-", "0").astype(float)

# 按照净额的绝对值进行排序
ranked_data = stock_individual_fund_flow_rank_df.iloc[stock_individual_fund_flow_rank_df["今日主力净流入-净额"].abs().argsort()[::-1]]

# 提取排名前一百只股票的名称和主力净流入-净额数据
top_100_stocks = ranked_data.head(80)
stocks = top_100_stocks["名称"]
net_inflows = top_100_stocks["今日主力净流入-净额"]
daily_change = top_100_stocks["今日涨跌幅"]

# 绘制图像
plt.figure(figsize=(12, 8))

# 根据净额的正负选择颜色
colors = ['red' if x >= 0 else 'green' for x in net_inflows]

bars = plt.bar(stocks, net_inflows, color=colors)
plt.ylabel('今日主力净流入-净额')
plt.title('主力流入净额')

# 在柱状图上标记每只股票的今日涨跌幅
for i, bar in enumerate(bars):
    if net_inflows.iloc[i] >= 0:
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height(),
                 f"{daily_change.iloc[i]}%",
                 ha='center', va='bottom', color='black', fontsize=8, fontweight='bold', rotation=60)
    else:
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height(),
                 f"{daily_change.iloc[i]}%",
                 ha='center', va='top', color='black', fontsize=8, fontweight='bold', rotation=30)

plt.xticks(rotation=90, fontsize=9)  # 使x轴标签垂直显示
plt.yticks(fontsize=8)  # 设置纵坐标刻度标签的大小
plt.ticklabel_format(axis='y', scilimits=(8, 8))  # 设置纵坐标的格式
plt.tight_layout()
plt.show()
