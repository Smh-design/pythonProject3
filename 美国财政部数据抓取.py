import requests
import pandas as pd
from datetime import datetime, timedelta


def fetch_debt_to_penny(start_date, end_date, page_size=1000):
    base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?fields=record_date,debt_held_public_amt,intragov_hold_amt,tot_pub_debt_out_amt,src_line_nbr"

    all_data = []
    page_number = 1

    while True:
        params = {
            "fields": "record_date,tot_pub_debt_out_amt",
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

            # 检查是否还有更多页
            if data['meta']['total-pages'] > page_number:
                page_number += 1
            else:
                break
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    df = pd.DataFrame(all_data)
    df['record_date'] = pd.to_datetime(df['record_date'])
    df['tot_pub_debt_out_amt'] = df['tot_pub_debt_out_amt'].astype(float)
    df = df.sort_values('record_date')

    return df


# 使用示例
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=3650)).strftime("%Y-%m-%d")  # 获取过去一年的数据

debt_data = fetch_debt_to_penny(start_date, end_date)

if debt_data is not None:
    print(debt_data.head())
    print(f"获取到的数据条数: {len(debt_data)}")

    # 计算一些基本统计信息
    print(f"平均债务金额: ${debt_data['tot_pub_debt_out_amt'].mean():,.2f}")
    print(f"最高债务金额: ${debt_data['tot_pub_debt_out_amt'].max():,.2f}")
    print(f"最低债务金额: ${debt_data['tot_pub_debt_out_amt'].min():,.2f}")

    # 可以进一步处理数据，例如保存为CSV
    debt_data.to_csv("us_debt_to_penny.csv", index=False)
    print("数据已保存到 us_debt_to_penny.csv")

    # 绘制简单的债务趋势图
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(debt_data['record_date'], debt_data['tot_pub_debt_out_amt'])
    plt.title('US Public Debt Trend')
    plt.xlabel('Date')
    plt.ylabel('Total Public Debt (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()