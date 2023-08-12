from telegram import Update, User, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def menu_keyboard():
    keyboard = []
    keyboard.append([
        InlineKeyboardButton(text = '💼 Мои позиции', callback_data='my_position'),
        ])
    keyboard.append([
        InlineKeyboardButton(text = '🟢 Создать лимит ордер', callback_data='create_limit'),
    ])
    keyboard.append([
        InlineKeyboardButton(text = '⚙️ Настройки', callback_data='settings'),
    ])
    keyboard.append([
        InlineKeyboardButton(text = '💶 Баланс', callback_data = 'balance'),
    ])
    return InlineKeyboardMarkup(keyboard)

def to_menu_keyboard():
    keyboard = []
    keyboard.append([
        InlineKeyboardButton(text = 'В меню', callback_data='menu'),
    ])
    return InlineKeyboardMarkup(keyboard)
