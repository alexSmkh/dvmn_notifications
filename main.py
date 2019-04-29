import requests
import datetime
from os.path import join
from os import getcwd
from os import getenv
from dotenv import load_dotenv
from telegram_bot import make_notifications


def send_request_on_devman(timestamp_for_tracking):
    dvmn_token = getenv('DEVMAN_TOKEN')
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    params = {'timestamp': timestamp_for_tracking}
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.ConnectionError:
        return None

    if response.ok:
        return response.json()


def main():
    load_dotenv(join(getcwd(), '.env'))
    timestamp_for_tracking = datetime.datetime.now().timestamp()
    while True:
        response_from_devman_api = send_request_on_devman(
            timestamp_for_tracking)
        if response_from_devman_api is None:
            continue
        if response_from_devman_api['status'] == 'found':
            solution_attempts = response_from_devman_api['new_attempts']
            timestamp_for_tracking = response_from_devman_api[
                'last_attempt_timestamp'
            ]
            make_notifications(solution_attempts)
        else:
            timestamp_for_tracking = response_from_devman_api[
                'timestamp_to_request'
            ]


if __name__ == '__main__':
    main()