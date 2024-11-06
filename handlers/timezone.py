import logging
import sqlite3

from telegram import Update
from telegram.ext import ContextTypes

from messages import send_message, send_acquire_timezone_message
from utility import get_chat_id, get_user_id, get_timezone

from db import create_user, update_timezone, get_user, connect_db

async def set_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat_id = get_chat_id(update)
    user_id = get_user_id(update)

    try:
        timezone = get_timezone(context)
    except:
        await send_message(
                bot,
                chat_id,
                "The timezone format is incorrect. Please refer to /help"
        )
        return

    with connect_db() as con:
        try:
            user = get_user(con, user_id)
            if user:
                update_timezone(con, user_id, timezone)
            else:
                create_user(con, user_id, timezone)
        except sqlite3.Error as e:
            logging.error(e)
            raise Exception("/settimezone command failed while updating db")

    await send_acquire_timezone_message(bot, chat_id, timezone)
