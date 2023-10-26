import json
import os
from dotenv import load_dotenv
import requests
import openai
from datetime import datetime, timezone, timedelta

load_dotenv()


getFeedbacksUrl = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'

api_key = os.getenv('WB_API_KEY')

openai.api_key = os.getenv("OPENAI_API_KEY")

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
        "Authorization": api_key
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


def sort_by_ai(text, valuation):
    prompt1 = f'Классифицируй отзыв. В ответ запиши в json в одну строчку без переносов строки с ключами tech, constr, strategy' \
              f'По умолчанию значение всех ключей 0.' \
              f'Если отзыв содежит претензии по пошиву, качеству материалов, информацию о том что изделие красит,' \
              f' садится при стирке или линяет, измени значение ключа tech на 1.' \
              f'Если отзыв содежит претензии связанные с размером, посадкой на фигуру, неверной длиной или шириной,' \
              f'измени значение ключа constr на 1.' \
              f'Если отзыв содежит претензии связанные с ценой или вопросы/предложения поразвитию ' \
              f'бренда в будущем (новые расцветки, размеры или ассортимент), измени значение ключа strategy на 1.' \
              f'Отзыв:' \
              f'{text}'

    prompt2 = f'Тебе будет предоставлен для анализа отзыв' \
              f'Оцени положительным или отрицательным является отзыв. При этом учитывай текст отзыва и оценку.' \
              f'Результат запиши в json в одну строчку без переносов строки в виде знаечения у ключа positive. Для положительного отзыва значение 1, для отрицательного 0.' \
              f'Отзыв:' \
              f'{text}' \
              f'Оценка (максимум 5): {valuation}'

    response1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt1}
        ],
        temperature=0,
        max_tokens=256
    )
    response2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt2}
        ],
        temperature=0,
        max_tokens=256
    )

    return [response1.choices[0].message.content, response2.choices[0].message.content]

def sort(feedbacks):

    for feefback in feedbacks:

        if len(feefback['text']) == 0:
            print(f"{feefback['createdDate']}    {feefback['id']}  {feefback['productValuation']}")
        else:
            print(f"\n{feefback['createdDate']}    {feefback['id']}   {feefback['productValuation']}  {feefback['text']}\n")
            result = sort_by_ai(feefback['text'], feefback['productValuation'])

            refs = json.loads(result[0].replace("'", ""))
            print(refs)

            positive = json.loads(result[1].replace("'", ""))
            print(positive)


sort(get_feedbacks(get_dates()['date_from'], get_dates()['date_to']))


