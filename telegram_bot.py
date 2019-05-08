from telegram.ext import Updater
from telegram.error import NetworkError
from os import environ


def send_notification_on_telegram(updater, user_id, notification):
    try:
        updater.bot.send_message(
            chat_id=user_id,
            text=notification)
    except NetworkError:
        return None


def make_notifications(solution_attempts):
    token = environ['TELEGRAM_TOKEN']
    user_id = environ['USER_ID']
    updater = Updater(token=token, use_context=True)

    for solution_attempt in solution_attempts:
        lesson_title = solution_attempt['lesson_title']
        lesson_url = solution_attempt['lesson_url']
        notification = f'Проверили работу "{lesson_title}"'
        if solution_attempt['is_negative']:
            notification += 'Можно приступать к следущему уроку!'
        else:
            notification += f'\nВ работе есть ошибки.\nСсылка на задачу: https://dvmn.org{lesson_url}'
        send_notification_on_telegram(updater, user_id, notification)
