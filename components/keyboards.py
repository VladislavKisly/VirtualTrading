from telegram import Update, User, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from database import Database

db = Database()

def menu_keyboard():
    keyboard = []
    keyboard.append([
        InlineKeyboardButton(text = '💼 Мои позиции', callback_data='my_positions'),
        ])
    keyboard.append([
        InlineKeyboardButton(text = '🟢 LONG', callback_data='create_position|long'),
        InlineKeyboardButton(text = '🔴 SHORT', callback_data='create_position|short')
    ])
    keyboard.append([
        InlineKeyboardButton(text = '💶 Баланс', callback_data = 'balance'),
    ])
    keyboard.append([InlineKeyboardButton(text = 'История', callback_data = 'history'),])

    return InlineKeyboardMarkup(keyboard)

def to_menu_keyboard():
    keyboard = []
    keyboard.append([
        InlineKeyboardButton(text = 'В меню', callback_data='menu'),
    ])

    return InlineKeyboardMarkup(keyboard)

def ticker_orders_keyboard(user_id: int, ticker: str):
    keyboard = []
    keyboard.append([InlineKeyboardButton(text = 'Объем   |   Цена   |   Сорона', callback_data='pass')])
    position = db.get_position(user_id, ticker)
    for x in position:
        keyboard.append([
            InlineKeyboardButton(text = f"{x['value']}   |   {x['price']}   |   {x['side']}", 
                                 callback_data = f"order|{ticker}|{x['value']}|{x['price']}|{x['side']}")])
    keyboard.append([
        InlineKeyboardButton(text = 'В меню', callback_data='menu'),
    ])

    return InlineKeyboardMarkup(keyboard)

def save_position():
    keyboard = []
    keyboard.append([
        InlineKeyboardButton(text = 'Создать ордер',
                                           callback_data = 'save_position'),
        InlineKeyboardButton(text = 'В меню', 
                                            callback_data = 'menu')
    ])

    return InlineKeyboardMarkup(keyboard)