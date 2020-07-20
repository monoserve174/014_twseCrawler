from flask import Flask, render_template, url_for, request
from twseCrawler import crawler_stock
import re

import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_id = request.form['stock_id']
        crawler_data = crawler_stock(int(stock_id))
        title = ["日期", "殖利率", "股利年度", "本益比", "股價淨值比", "財報年/季"]
        pd_data = pd.DataFrame(crawler_data, columns=title)
        date = []

        # 將民國yyy年mm月dd日轉完西元yyyy-mm-dd
        for date_data in pd_data['日期']:
            date_data = re.findall('\d{3}|\d{2}', date_data)
            date_data = '-'.join(str(int(item) + 1911) if item == date_data[0] else item for item in date_data)
            date.append(date_data)

        # 將字串轉為日期
        pd_data['日期'] = pd.DataFrame(date)
        pd_data['日期'] = pd.to_datetime(pd_data['日期'])
        del date, date_data, title

        # 藉由日期重新排序，並重新編號(ignore_index)
        pd_data = pd_data.sort_values(by='日期', ignore_index=True)

        # 將日期轉回字串
        pd_data['日期'] = pd_data['日期'].apply(lambda x: x.strftime('%Y-%m-%d'))

        stock_data = {
            'chart': {
                'type': 'line',
                'zoomType': 'x'
            },
            'title': {
                'text': '最近六個月的殖利率、本益比與股價淨值比'
            },
            'yAxis': {
                'title': {
                    'text': 'values'
                }
            },

            'xAxis': {
                'title': {
                    'text': 'date'
                },
                'categories': pd_data['日期'].to_list()
            },

            'legend': {
                'layout': 'vertical',
                'align': 'right',
                'verticalAlign': 'middle'
            },

            'series': [{
                'name': '殖利率',
                'data': [float(item) for item in pd_data['殖利率'].to_list()]
            }, {
                'name': '本益比',
                'data': [float(item) for item in pd_data['本益比'].to_list()]
            }, {
                'name': '股價淨值比',
                'data': [float(item) for item in pd_data['股價淨值比'].to_list()]
            }],

            'responsive': {
                'rules': [{
                    'condition': {
                        'maxWidth': 500
                    },
                    'chartOptions': {
                        'legend': {
                            'layout': 'horizontal',
                            'align': 'center',
                            'verticalAlign': 'bottom'
                        }
                    }
                }]
            }
        }

        return render_template('index.html', stock_data=stock_data)
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
