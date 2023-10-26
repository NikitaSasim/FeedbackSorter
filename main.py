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
    skip = -50
    response_len = 50
    feedbacks = []

    while response_len == 50:
        skip += 50
        params = {
            "isAnswered": "true",
            "take": 50,
            "skip": skip,
            "dateFrom": date_from,
            "dateTo": date_to
        }

        response = requests.get(getFeedbacksUrl, params=params, headers=headers).json()['data']['feedbacks']
        response_len = len(response)

        if response_len > 0:
            feedbacks += response
    return feedbacks

def sort(feedbacks):

    for feefback in feedbacks:

        if len(feefback['text']) == 0:
            print(f"{feefback['createdDate']}    {feefback['id']}  {feefback['productValuation']}")
        else:
            print(f"{feefback['createdDate']}    {feefback['id']}  {feefback['text']}")
# print(getFeedbacks())


sort(get_feedbacks(get_dates()['date_from'], get_dates()['date_to']))


