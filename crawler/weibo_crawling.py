import requests
from pyquery import PyQuery as pq
import datetime
from datetime import date, timedelta
from time import strptime
import pandas as pd


def get_html(url):
    response = requests.get(url=url)
    res = response.json()

    return res


# 解析數據
def parse_html(html, day):
    cards = html['data']['cards']

    created_date = list()
    title = list()
    content = list()
    i = 0

    for card in (cards):
        weibo = dict()
        mblog = card['mblog']

        # convert date format: Dec 06-> 12/06
        month = str(mblog['created_at'][4:7])
        month_number = strptime(month, '%b').tm_mon
        created_date.append(str(month_number) + '/' + str(mblog['created_at'][8:10]))
        # print(created_date)
        if created_date[i] != day:
            break

        weibo['post'] = pq(mblog['text']).text()
        # use '】' to separate tile and content
        if weibo['post'].find('】') > 0:
            end_title = weibo['post'].find('】')
            title.append(weibo['post'][1:end_title])
            content.append(weibo['post'][end_title + 1:])
        else:
            continue
        i = i + 1

    headers = ['Date', 'Title', 'Content']
    df = pd.DataFrame(list(zip(created_date, title, content)), columns=headers)
    # print(df)
    return df


if __name__ == '__main__':
    today = date.today() - timedelta(days=1)
    print(today)
    daytoday = today.strftime("%m/%d")
    print(daytoday)

    new_df = []
    results=pd.DataFrame()
    for i in range(1, 20):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1618051664&containerid=1076031618051664&page=' + str(
            i)
        html = get_html(url)
        weibo = parse_html(html, daytoday)
        results = pd.concat([results, weibo], axis=0).reset_index(drop=True)

    print(results)
    file_day = today.strftime("%m_%d")
    results.to_csv(file_day+"_weibo_result.csv", index=False)


