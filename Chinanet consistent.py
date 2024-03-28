import akshare as ak
import pandas as pd

# 获取沪深300历史数据
index_df = ak.index_zh_a_hist(symbol="399006")


# 计算连续涨跌的天数和每次涨跌的幅度
def calculate_continuous_change(data):
    continuous_days = 0
    cumulative_change = 0
    previous_change = None
    data['连续涨跌天数'] = None
    data['连续涨跌幅度'] = None

    for index, row in data.iterrows():
        change = row['涨跌幅']
        if previous_change is None or change * previous_change <= 0:
            continuous_days = 1 if change > 0 else -1
            cumulative_change = change
        else:
            cumulative_change += change
            continuous_days += 1 if change > 0 else -1
        data.at[index, '连续涨跌天数'] = continuous_days
        data.at[index, '连续涨跌幅度'] = cumulative_change
        previous_change = change
    return data


index_df = calculate_continuous_change(index_df)


# 提取连续涨或跌的数据组并重排
def rearrange_data(data):
    result_df = pd.DataFrame()
    trend_groups = []
    current_group = []
    for index, row in data.iterrows():
        continuous_days = row['连续涨跌天数']
        if continuous_days is None or continuous_days == 0:
            continue
        if not current_group or continuous_days * current_group[-1]['连续涨跌天数'] > 0:
            current_group.append(row)
        else:
            trend_groups.append(current_group)
            current_group = [row]
    if current_group:
        trend_groups.append(current_group)

    for idx, group in enumerate(trend_groups, start=1):
        group_df = pd.DataFrame(group).reset_index(drop=True)
        group_df.insert(0, '组序号', idx)
        result_df = pd.concat([result_df, group_df], ignore_index=True)
    return result_df


result_df = rearrange_data(index_df)

print(result_df)

# 导出到 Excel 文件
data = result_df
df = pd.DataFrame(data)
result_df = pd.DataFrame(columns=range(df['连续涨跌天数'].min(), df['连续涨跌天数'].max() + 1))
# 遍历原始数据，将涨跌幅数据按照连续涨跌天数分类到result_df中
for index, row in df.iterrows():
    days = row['连续涨跌天数']
    magnitude = row['连续涨跌幅度']
    if days not in result_df.columns:
        result_df[days] = None
    result_df.at[index, days] = magnitude

# 添加日期列
date_column = index_df['日期']
result_df.insert(0, '日期', date_column)

print(result_df)
# Export data to Excel
excel_file = "连续涨跌数据.xlsx"
result_df.to_excel(excel_file, index=False)

print("数据已成功导出到 Excel 文件:", excel_file)