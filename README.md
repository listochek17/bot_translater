# Описание проекта

Этот репозиторий содержит простой Telegram-бот для перевода текста. Бот позволяет пользователю выбрать язык-источник и язык-приёмник, ввести текст и получить перевод. Все переводы сохраняются в локальную базу данных SQLite для просмотра истории.

Ключевые возможности
- Выбор языка-источника и языка-приёмника через ReplyKeyboard
- Перевод текста с помощью библиотеки `googletrans`
- Сохранение истории переводов в `bot.db` (SQLite)

Где смотреть код
- Основная логика: `bot_translater/main.py`
- Клавиатуры: `bot_translater/keyboards.py`
- Работа с БД: `bot_translater/database.py`

Короткая инструкция по запуску
1) Установите зависимости и активируйте виртуальное окружение в папке `bot_translater`:
```powershell
cd 'C:\Users\Улугбек\Desktop\Githab_correcting\bot_translater'
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
2) Создайте `.env` с TOKEN:
```
TOKEN=<ваш_токен_бота>
```
3) Запустите бота:
```powershell
python main.py
```

Примечание
- Для стабильной работы в продакшне рассмотрите использование официального API перевода (Google Cloud Translate) вместо `googletrans`.

