import requests
import datetime
from telegram_bot import send_notifications


def fetch_reviews():
    url = 'https://dvmn.org/api/long_polling/'
    ninety_seconds = 90
    first_timestamp = datetime.datetime.now().timestamp()
    headers = {'Authorization': 'Token 4b6cbc3d2203e468b0529ecaac824e14378abb9f'}
    params = {'timestamp': first_timestamp}
    while True:
        try:
            response = requests.get(url, headers=headers, params=params).json()
        except requests.exceptions.Timeout:
            continue
        if response['status'] == 'found':
            notifications = response['new_attempts']
            last_notification = notifications[-1]
            time_shift = 0.000001
            params['timestamp'] = last_notification['timestamp'] + time_shift
            send_notifications(notifications)
        else:
            params['timestamp'] += ninety_seconds


def main():
    fetch_reviews()


if __name__ == '__main__':
    main()