import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone, timedelta

load_dotenv()


getFeedbacksUrl = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'

apiKey = os.getenv('WB_API_KEY')

def get_dates():
    today = datetime.now(timezone.utc)
    # tz = timezone(offset=timedelta())
    # today = tz.utcoffset(today)
    date_from = datetime(
        year=today.year,
        month=today.month,
        day=today.day-1,
        hour=0,
        minute=0,
        second=0,
        tzinfo=timezone.utc
    )
    date_to = datetime(
        year=today.year,
        month=today.month,
        day=today.day-1,
        hour=23,
        minute=59,
        second=59,
        tzinfo=timezone.utc
    )
    date_from = int(date_from.timestamp())
    date_to = int(date_to.timestamp())
    dates = {
        'date_from': date_from,
        'date_to': date_to
    }

    return dates


print(get_dates())


def get_feedbacks(date_from, date_to):
    headers = {
        "Authorization": apiKey
    }

    params = {
        "isAnswered": "true",
        "take": 80,
        "skip": 0,
        "dateFrom": date_from,
        "dateTo": date_to
    }

    response = requests.get(getFeedbacksUrl, params=params, headers=headers)
    # return response.json().data.feedbacks
    feedbacks = response.json()['data']['feedbacks']
    return feedbacks


for feefback in get_feedbacks(get_dates()['date_from'], get_dates()['date_to']):
    print(f"{feefback['createdDate']}    {feefback['id']}")
# print(getFeedbacks())



