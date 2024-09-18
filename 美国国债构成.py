import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta


def fetch_debt_to_penny(start_date, end_date, page_size=1000):
    base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_1"

    all_data = []
    page_number = 1

    while True:
        params = {
            "fields": "record_date,security_type_desc,security_class_desc,debt_held_public_mil_amt,intragov_hold_mil_amt,total_mil_amt,record_calendar_year,record_calendar_quarter,record_calendar_month,record_calendar_day",
            "filter": f"record_date:gte:{start_date},record_date:lte:{end_date}",
            "sort": "-record_date",
            "format": "json",
            "page[number]": page_number,
            "page[size]": page_size
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['data'])

            if data['meta']['total-pages'] > page_number:
                page_number += 1
            else:
                break
        else:
            print(f"Request failed, status code: {response.status_code}")
            return None

    df = pd.DataFrame(all_data)
    df['record_date'] = pd.to_datetime(df['record_date'])
    df['total_mil_amt'] = pd.to_numeric(df['total_mil_amt'], errors='coerce')
    df = df.sort_values('record_date')

    return df


# 使用示例
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=3650)).strftime("%Y-%m-%d")  # 获取过去10年的数据

debt_data = fetch_debt_to_penny(start_date, end_date)

if debt_data is not None and not debt_data.empty:
    print(debt_data.head())
    print(f"获取到的数据条数: {len(debt_data)}")

    # 保存为CSV
    debt_data.to_csv("us_debt_outstanding.csv", index=False)
    print("数据已保存到 us_debt_outstanding.csv")

    # 数据分组和绘图
    grouped_data = debt_data.groupby(['record_date', 'security_class_desc'])['total_mil_amt'].sum().unstack()

    # 移除可能存在的下划线开头的列
    grouped_data = grouped_data.loc[:, ~grouped_data.columns.str.startswith('_')]

    # 检查是否有足够的数据进行绘图
    if not grouped_data.empty and grouped_data.shape[1] > 0:
        plt.figure(figsize=(14, 8))
        ax = sns.lineplot(data=grouped_data)

        # 添加每条线的注释
        for security_class in grouped_data.columns:
            y = grouped_data[security_class].dropna()
            if not y.empty:
                last_date = y.index[-1]
                last_value = y.iloc[-1]
                ax.annotate(
                    security_class,
                    xy=(last_date, last_value),
                    xytext=(last_date, last_value + (last_value * 0.05)),  # Offset annotation
                    textcoords='data',
                    ha='center',
                    va='bottom',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white'),
                    arrowprops=dict(facecolor='black', shrink=0.05)
                )

        plt.title('Total Outstanding Debt by Security Class Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Amount (in million USD)')
        plt.legend(title='Security Class', loc='upper left', bbox_to_anchor=(1, 1))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
    else:
        print("分组后的数据为空或没有有效的列，无法绘图。")
else:
    print("获取的数据为空，无法进行分析和绘图。")
