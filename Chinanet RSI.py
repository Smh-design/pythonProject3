import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 获取数据
data = ak.index_zh_a_hist(symbol="399006", period="daily", start_date="20100601", end_date="20240521")

# 数据预处理
data['涨跌幅'] = pd.to_numeric(data['涨跌幅']) / 100
data['up'] = data['涨跌幅'].apply(lambda x: x if x > 0 else 0)
data['down'] = data['涨跌幅'].apply(lambda x: -x if x < 0 else 0)
data['avg_up'] = data['up'].rolling(window=14).mean()
data['avg_down'] = data['down'].rolling(window=14).mean()
data['RS'] = data['avg_up'] / data['avg_down']
data['RSI'] = 100 - (100 / (1 + data['RS']))

# 选择最近的30个数据点
recent_data = data.tail(30)

# 绘图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax1.plot(recent_data['日期'], recent_data['收盘'], color='b')
ax1.set_ylabel('Close Price', color='b')

ax2.plot(recent_data['日期'], recent_data['RSI'], color='r')
ax2.set_ylabel('RSI', color='r')

ax2.axhline(y=70, color='gray', linestyle='--')
ax2.axhline(y=30, color='gray', linestyle='--')

plt.xticks(rotation=90)
plt.title('创业板指 Close Price and RSI (Last 30 days)')
plt.tight_layout()
plt.show()