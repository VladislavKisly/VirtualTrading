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
from database import Database

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

async def short_handle(update: Update, context: CallbackContext):
    pass

async def long_handle(update: Update, context: CallbackContext):
    pass

async def balance_handle(update: Update, context: CallbackContext):
    
    text = messages.balance_text(update.callback_query.from_user.id)
    keyboard = keyboards.to_menu_keyboard()

    await update.callback_query.edit_message_text(text, 
                                                    ParseMode.HTML, 
                                                        reply_markup=keyboard)

def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(telegram_token)
        .build()
    )

    user_filter = filters.ALL

    application.add_handler(CommandHandler("start", start_handle, filters=user_filter))
    application.add_handler(CallbackQueryHandler(balance_handle, pattern='^balance'))
    application.add_handler(CallbackQueryHandler(menu_handle, pattern='^menu'))

    
    application.run_polling(drop_pending_updates = True, stop_signals=None)

if __name__ == "__main__":
    run_bot()
