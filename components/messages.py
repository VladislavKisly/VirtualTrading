from database import Database

db = Database()

def menu_text():
    text = 'Выбери действие'
    return text

def my_position():
    pass

def long_position():
    pass

def short_position():
    pass

def balance_text(user_id: int):
    user = db.get_user(user_id)
    start_summ = user['start_summ']
    profit = user['profit']
    balance = user['start_summ'] + user['profit']
    profit_prc = (profit * 100) / start_summ
    registration_date = user['registration_date']
    text = f'Баланс: <b>{balance}</b>\n\n'
    text += f'Стартовая сумма: <b>{start_summ}</b>\n'
    text += f'Профит $: <b>{profit}</b>\n'
    text += f'Профит %: <b>{profit_prc}</b>\n'
    text += f'Дата начала: <b>{registration_date}</b>\n'
    return text
