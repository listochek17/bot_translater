"""Помощники для клавиатур бота-перевожика.

Файл был создан как корректное имя вместо `keyboerds.py`.
Содержит две функции: основную клавиатуру и меню языков.
"""

from telebot import types
from googletrans import LANGCODES


def start_kb():
    """Главная клавиатура с кнопками Start и History."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton(text="Start"),
        types.KeyboardButton(text="History")
    )

    return markup


def land_menu():
    """Создаёт клавиатуру со списком доступных языков.

    Ключи LANGCODES приводятся к title-case для отображения пользователю.
    Сортировка даёт предсказуемый порядок кнопок.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = []
    for lang in sorted(LANGCODES.keys()):
        button = types.KeyboardButton(text=lang.title())
        buttons.append(button)
    markup.add(*buttons)
    return markup

