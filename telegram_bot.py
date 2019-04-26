from telegram.ext import Updater
from telegram.error import NetworkError
from dotenv import load_dotenv
from os import getenv
from os.path import join
from os import getcwd


def send_notifications(notifications):
    load_dotenv(join(getcwd(), '.env'))
    token = getenv('TOKEN')
    proxy_url = getenv('PROXY')
    user_id = getenv('USER_ID')
    request_kwargs = {'proxy_url': proxy_url}
    updater = Updater(token, request_kwargs=request_kwargs)

    for notification in notifications:
        lesson_title = notification['lesson_title']
        lesson_url = notification['lesson_url']
        message = f'Проверили работу "{lesson_title}"'
        if notification['is_negative'] is False:
            message += f'\nВ работе есть ошибки.\nСсылка на задачу: https://dvmn.org{lesson_url}'
        else:
            message += 'Можно приступать к следущему уроку!'

        try:
            updater.bot.send_message(
                chat_id=user_id,
                text=message)
        except NetworkError as error:
            print(error)