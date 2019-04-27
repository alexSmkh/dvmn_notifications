from telegram.ext import Updater
from telegram.error import NetworkError
from os import getenv


def send_notification_on_telegram(updater, user_id, notification):
    try:
        updater.bot.send_message(
            chat_id=user_id,
            text=notification)
    except NetworkError:
        return None


def make_notifications(solution_attempts):
    token = getenv('TELEGRAM_TOKEN')
    proxy_url = getenv('PROXY')
    user_id = getenv('USER_ID')
    request_kwargs = {'proxy_url': proxy_url}
    updater = Updater(token, request_kwargs=request_kwargs)

    for solution_attempt in solution_attempts:
        lesson_title = solution_attempt['lesson_title']
        lesson_url = solution_attempt['lesson_url']
        notification = f'Проверили работу "{lesson_title}"'
        if solution_attempt['is_negative']:
            notification += 'Можно приступать к следущему уроку!'
        else:
            notification += f'\nВ работе есть ошибки.\nСсылка на задачу: https://dvmn.org{lesson_url}'
        send_notification_on_telegram(updater, user_id, notification)
