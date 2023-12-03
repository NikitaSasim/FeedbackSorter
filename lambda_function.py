from main import sort, get_feedbacks, get_dates


def lambda_handler(event, context):
    sort(get_feedbacks(get_dates()['date_from'], get_dates()['date_to']))

