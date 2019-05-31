import datetime
import logging
from time import sleep
from os import environ
from logs_handler import get_logger

import requests
from telegram.ext import Updater
from telegram.error import NetworkError
from dotenv import load_dotenv


logger = get_logger('TelegramLogger')


def send_notification_on_telegram(updater, user_id, message):
    try:
        updater.bot.send_message(
            chat_id=user_id,
            text=message)
    except NetworkError as error:
        logger.info(f'Бот упал с ошибкой: {error}.')
        logger.warning(NetworkError, exc_info=True)
        return None


def make_notifications(solution_attempts):
    token = environ['TELEGRAM_TOKEN']
    user_id = environ['USER_ID']
    updater = Updater(token=token)
    for solution_attempt in solution_attempts:
        lesson_title = solution_attempt['lesson_title']
        lesson_url = solution_attempt['lesson_url']
        notification = f'Проверили работу "{lesson_title}". '
        if not solution_attempt['is_negative']:
            notification += 'Можно приступать к следующему уроку!'
        else:
            notification += f'\nВ работе есть ошибки.\nСсылка назадачу: https://dvmn.org{lesson_url}'
        send_notification_on_telegram(updater, user_id, notification)


def send_request_on_devman(timestamp_for_tracking):
    dvmn_token = environ['DEVMAN_TOKEN']
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    params = {'timestamp': timestamp_for_tracking}
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.ConnectionError as error:
        logger.info(f'Бот упал с ошибкой: {error}.')
        logger.warning(error, exc_info=True)
        return None

    if not response.ok:
        logger.info(f'Бот упал с ошибкой.')
        logger.warning(requests.exceptions.HTTPError)
        response.raise_for_status()

    return response.json()


def main():
    load_dotenv()
    logger.info('Бот запущен!')
    timestamp_for_tracking = datetime.datetime.now().timestamp()
    while True:
        response_from_devman_api = send_request_on_devman(
            timestamp_for_tracking)
        if response_from_devman_api is None:
            sleep(30)
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
