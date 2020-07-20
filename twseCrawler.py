# %%
# Load Package
import json
import time
import datetime
import requests


def crawler_stock(stock_id):
    my_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
               'Chrome/83.0.4103.116 Mobile Safari/537.36'
    headers = {'user-agent': my_agent}
    params = {'response': 'json', 'stockNo': f'{stock_id}'}

    # 設置半年時間
    dates = []
    base_date = datetime.date.today().replace(day=1)
    for _ in range(6):
        dates.append(base_date.strftime('%Y%m%d'))
        base_date -= datetime.timedelta(days=1)
        base_date = base_date.replace(day=1)

    stock_data = []
    for date in dates:
        url = 'https://www.twse.com.tw/exchangeReport/BWIBBU'
        params['date'] = date
        data_res = requests.get(url=url, headers=headers, params=params)
        month_data = json.loads(data_res.text)
        for day_data in month_data['data']:
            stock_data.append(day_data)
    return stock_data