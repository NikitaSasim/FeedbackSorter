import os
from dotenv import load_dotenv
import requests

load_dotenv()


getFeedbacksUrl = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'

apiKey = os.getenv('WB_API_KEY')


def getFeedbacks():
    headers = {
        "Authorization": apiKey
    }

    params = {
        "isAnswered": "true",
        "take": 80,
        "skip": 0,
        "dateFrom": 1698184800,
        "dateTo": 1698271200
    }

    response = requests.get(getFeedbacksUrl, params=params, headers=headers)
    # return response.json().data.feedbacks
    return response.json()['data']['feedbacks']


for feefback in getFeedbacks():
    if len(feefback['text']) > 0:
        print(feefback['text'])
# print(getFeedbacks())



