from database import Database

db = Database()

def menu_text():
    text = 'Выбери действие'
    return text

def my_position():
    text = 'Введи тикер по которому хочешь посмотреть свои позиции, например <b>BTCUSDT</b>'
    return text

def ticker_orders():
    text = 'Твои позиции'
    return text

def ticker_not_found():
    text = 'Ордеров по данному тикеру не найдено.\nВозможно этот тикер не существует, попробуй другой.\nНапример <b>BTCUSDT</b>'
    return text

def create_position():
    text = 'Введи тикер, для которого хочешь выстовить ордер'
    return text

def create_position_price_info():
    text = 'Введи цену, на который хочешь выставить ордер'
    return text

def create_position_profit_info():
    text = 'Введи цену, на которую хочешь выставить Take-Profit'
    return text

def create_position_stop_info():
    text = 'Введи цену, на которую хочешь выставить Stop-Loss'
    return text

def create_position_value_info():
    text = 'Введи объем, который хочешь использовать для позиции'
    return text

def create_position_leverage_info():
    text = 'Введи плечо, которое хочешь выставить для этой позиции'
    return text

def create_position_save(user_data: dict):
    text = f'{user_data}'
    return text

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
