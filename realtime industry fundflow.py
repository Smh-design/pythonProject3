import akshare as ak
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# Retrieve data
stock_sector_fund_flow_rank_df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
print(stock_sector_fund_flow_rank_df.columns.tolist())
A = "今日主力净流入-净额"
# Extract columns
net_inflow = stock_sector_fund_flow_rank_df[A]
names = stock_sector_fund_flow_rank_df['名称']
daily_change = stock_sector_fund_flow_rank_df['今日涨跌幅']

# Sort by absolute net inflow values
sorted_indices = sorted(range(len(net_inflow)), key=lambda k: abs(net_inflow[k]), reverse=True)
net_inflow_sorted = [net_inflow[i] for i in sorted_indices[:50]]
names_sorted = [names[i] for i in sorted_indices[:50]]
daily_change_sorted = [daily_change[i] for i in sorted_indices[:50]]
colors_sorted = ['red' if x >= 0 else 'green' for x in net_inflow_sorted]

# Create a suitable plot
plt.figure(figsize=(15, 8))

# Plot bars
bars = plt.bar(names_sorted, net_inflow_sorted, color=colors_sorted)

# Annotate bars with daily change values
for bar, change, inflow, color in zip(bars, daily_change_sorted, net_inflow_sorted, colors_sorted):
    # Determine vertical alignment based on the sign of net inflow
    va = 'bottom' if inflow >= 0 else 'top'
    # Determine the position of the annotation based on the sign of net inflow
    position = bar.get_height() if inflow >= 0 else bar.get_height() - 0.03
    # Determine text color based on the sign of daily change
    text_color = 'red' if change >= 0 else 'green'
    plt.text(bar.get_x() + bar.get_width() / 2,
             position,
             f'{change:.2f}%',
             ha='center', va=va, color=text_color, rotation=30)

plt.xlabel('行业', fontsize=14)
plt.ylabel(f'{A} (亿元)', fontsize=14)  # Added unit to the y-axis label

# Set y-axis ticks to show units in 亿元
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0f}'.format(x / 1e8)))

# Set x-axis labels color based on the sign of net inflow
for tick, color in zip(plt.gca().get_xticklabels(), colors_sorted):
    tick.set_color(color)
    tick.set_rotation(90)  # Rotate x-axis labels by 90 degrees

plt.tight_layout()
plt.title(A)
plt.show()