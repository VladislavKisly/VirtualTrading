import os
import logging
import traceback
import html
import random
import threading
import telebot
import time
import json
import threading
from datetime import datetime

import telegram
from telegram import Update, User, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    filters
)
from telegram.constants import ParseMode, ChatAction

from config import telegram_token
from components import keyboards, messages
from utils.exchanges.binance import BinanceData
from database import Database

TICKER_POS = range(1)

GET_TICKER, GET_PRICE, GET_TAKE_PROFIT, \
GET_STOP_LOSS, GET_VALUE, \
GET_LEVERAGE = range(6)

async def start_handle(update: Update, context: CallbackContext):
    text = messages.menu_text()
    keyboard = keyboards.menu_keyboard()

    Database().registration(update.message.from_user.id, 
                                update.message.from_user.first_name)

    await update.message.reply_text(text,
                                reply_markup=keyboard)

async def menu_handle(update: Update, context: CallbackContext):
    text = messages.menu_text()
    keyboard = keyboards.menu_keyboard()
                            
    await update.callback_query.edit_message_text(text, 
                                            reply_markup=keyboard)


async def balance_handle(update: Update, context: CallbackContext):
    text = messages.balance_text(update.callback_query.from_user.id)
    keyboard = keyboards.to_menu_keyboard()

    await update.callback_query.edit_message_text(text, 
                                                    ParseMode.HTML, 
                                                        reply_markup=keyboard)
    
async def my_positions_handle(update: Update, context: CallbackContext):
    text = messages.my_position()
    keyboard = keyboards.to_menu_keyboard()

    await update.callback_query.edit_message_text(text, 
                                                    ParseMode.HTML,
                                                        reply_markup=keyboard)
    return TICKER_POS

async def create_position(update: Update, context: CallbackContext):
    side = None

    text = messages.create_position()
    keyboard = keyboards.to_menu_keyboard()

    if update.callback_query == None:
        side = context.user_data['side']
        await update.message.reply_text(text,
                                            reply_markup=keyboard)
    else:
        side = update.callback_query.data.split('|')[1]
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    context.user_data['side'] = side
    return GET_TICKER

async def get_ticker_create_position(update: Update, context: CallbackContext):
    # TODO: Проверка на существование
    ticker = update.message.text
    data = BinanceData().get_prices(ticker)

    if type(data) is not dict: await create_position(update, context)
    
    context.user_data['ticker'] = ticker
    text = messages.create_position_price_info()
    keyboard = keyboards.to_menu_keyboard()
    
    await update.message.reply_text(text, 
                                        reply_markup=keyboard)
    
    return GET_PRICE

async def get_price(update: Update, context: CallbackContext):
    price = update.message.text
    context.user_data['price'] = price
    
    text = messages.create_position_profit_info()
    keyboard = keyboards.to_menu_keyboard()
    
    await update.message.reply_text(text,
                                        reply_markup=keyboard)
    
    return GET_TAKE_PROFIT

async def get_take_profit(update: Update, context: CallbackContext):
    profit = update.message.text
    context.user_data['take_profit'] = profit
    
    text = messages.create_position_stop_info()
    keyboard = keyboards.to_menu_keyboard()
    
    await update.message.reply_text(text,
                                        reply_markup=keyboard)
    
    return GET_STOP_LOSS

async def get_stop_loss(update: Update, context: CallbackContext):
    # TODO: Проверка на больше меньше профита
    stop_loss = update.message.text
    context.user_data['stop_loss'] = stop_loss
    
    text = messages.create_position_value_info()
    keyboard = keyboards.to_menu_keyboard()
   
    await update.message.reply_text(text,
                                        reply_markup=keyboard)
    
    return GET_VALUE
    
async def get_value(update: Update, context: CallbackContext):
    # TODO: Проверка на использованный объем
    value = update.message.text
    context.user_data['value'] = value
    
    text = messages.create_position_leverage_info()
    keyboard = keyboards.to_menu_keyboard()
    
    await update.message.reply_text(text,
                                        reply_markup=keyboard)
    
    return GET_LEVERAGE

async def get_leverage(update: Update, context: CallbackContext):
    leverage = update.message.text
    
    try:
        if int(leverage) > 100: 
            pass
        else:
            pass
    except:
        pass

    context.user_data['leverage'] = leverage
    text = messages.create_position_save(context.user_data)
    keyboard = keyboards.save_position()
    await update.message.reply_text(text,
                                        reply_markup=keyboard)
    return ConversationHandler.END
    

async def get_ticker_handle(update: Update, context: CallbackContext):
    ticker = update.message.text
    positions = Database().get_position(update.message.from_user.id, ticker)
    
    if len(positions) == 0:
        text = messages.ticker_not_found()
        keyboard = keyboards.to_menu_keyboard()
        await update.message.reply_text(text,
                                            ParseMode.HTML,
                                                reply_markup=keyboard)
    else:
        text = messages.ticker_orders()
        keyboard = keyboards.ticker_orders_keyboard(update.message.from_user.id, 
                                                        ticker)
        await update.message.reply_text(text, 
                                            ParseMode.HTML,
                                                reply_markup=keyboard)
        
def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(telegram_token)
        .build()
    )

    user_filter = filters.ALL

    get_positions_handlers = ConversationHandler(
        entry_points=[CallbackQueryHandler(my_positions_handle, pattern = '^my_positions')],
        states = {
            TICKER_POS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, get_ticker_handle
                ),
            ],
        },
        fallbacks=[CallbackQueryHandler(menu_handle, pattern='^menu')],
    )
    
    create_position_handlers = ConversationHandler(
        entry_points=[CallbackQueryHandler(create_position, pattern='^create_position')],
        states={
            GET_TICKER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, get_ticker_create_position
                ),
            ],
            GET_PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, get_price
                ),
            ],
            GET_TAKE_PROFIT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, get_take_profit
                ),
            ],
            GET_STOP_LOSS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, get_stop_loss
                ),
            ],
            GET_VALUE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, get_value
                ),
            ],
            GET_LEVERAGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, get_leverage
                ),
            ],
        },
        fallbacks=[CallbackQueryHandler(menu_handle, pattern='^menu')]
    )
    
    application.add_handler(get_positions_handlers)
    application.add_handler(create_position_handlers)
    application.add_handler(CommandHandler("start", start_handle, filters=user_filter))
    application.add_handler(CallbackQueryHandler(balance_handle, pattern='^balance'))
    application.add_handler(CallbackQueryHandler(my_positions_handle, pattern='^my_positions'))
    application.add_handler(CallbackQueryHandler(create_position, pattern='^create_position'))

    application.add_handler(CallbackQueryHandler(menu_handle, pattern='^menu'))

    
    application.run_polling(drop_pending_updates = True, stop_signals=None)

if __name__ == "__main__":
    run_bot()
