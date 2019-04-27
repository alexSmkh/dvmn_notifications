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
        response = requests.get(url, headers=headers, params=params).json()
        return response
    except requests.exceptions.Timeout:
        return None


def fetch_solution_attempts():
    timestamp_for_tracking = datetime.datetime.now().timestamp()
    while True:
        response_from_devman_api = send_request_on_devman(timestamp_for_tracking)
        if response_from_devman_api is None:
            continue
        if response_from_devman_api['status'] == 'found':
            solution_attempts = response_from_devman_api['new_attempts']
            last_solution_attempt = solution_attempts[-1]
            time_shift = 0.000001
            timestamp_for_tracking = last_solution_attempt['timestamp'] + time_shift
            make_notifications(solution_attempts)
        else:
            timestamp_for_tracking = response_from_devman_api['timestamp_to_request']


def main():
    fetch_solution_attempts()


if __name__ == '__main__':
    load_dotenv(join(getcwd(), '.env'))
    main()