# Уведомления о проверке работ для Devman
Скрипт отправляет уведомление в Telegram, как только задача будет проверена.

### Как установить 
Должен быть установлен `python3`. Затем используйте `pip`(или `pip3`, 
 если есть конфликт с `Python2`) для установки зависимостей: 
 ```bash
 pip install -r requirements.txt
 ```
 
 
 ### Как настроить
[Узнайте](https://dvmn.org/api/docs/) свой токен для DevmanAPI. 

Создайте telegram бота и получите API-ключ. [Как обойти блокировку Telegram](https://bigpicture.ru/?p=913797),
 
[Как создать бота и получить токен](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)

Узнайте свой id, написав в Telegram специальному боту: @userinfobot 

Создайте чат со своим ботом.


Зарегистрируйте аккаунт [Heroku](https://www.heroku.com/), чтобы задеплоить бота.
 Создайте приложение. Во вкладке Deploy найдите пункт "App connected to GitHub" и присоедините
 свой репозиторий с ботом. В пункте "Manual deploy" кликните по кнопке, чтобы выполнить деплой.


 Перейдите во вкладку "Settings". В пункте "Config Vars" введите телеграм токен,
 devman токен  и user_id.
 
 Перейдите во вкладку "Resources" и напротив строки `bot python3 main.py`  кликните по переключателю.
```txt
TELEGRAM_TOKEN='ваш токен'
DEVMAN_TOKEN='ваш токен'
USER_ID='12345'
```

### Как запустить
```bash
python3 main.py
```

### Цель проекта
 Код написать в образовательных целях на онлайн-курсе для веб-разработчиков 
 [dvmn.org](dvmn.org)