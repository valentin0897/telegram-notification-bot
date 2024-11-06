import logging
import sqlite3
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import ContextTypes

from messages import send_message, send_acquire_reminder_message
from messages import send_timezone_reminder_message
from utility import get_chat_id, get_user_id
from utility import get_datetime, get_notification_message

from db import get_timezone_by_user_id, connect_db

async def callback_reminder(context: ContextTypes.DEFAULT_TYPE):
    if context.job is not None and context.job.chat_id is not None:
        chat_id = context.job.chat_id
        bot = context.bot
        data = context.job.data
        if isinstance(data, dict) and dict:
            text = data["text"]
        else:
            text = "Alarm"

        await send_message(bot, chat_id, text)
    else:
        raise Exception("There is no job attached to this callback")


async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat_id = get_chat_id(update)
    user_id = get_user_id(update)

    try:
        with connect_db() as con:
            timezone = get_timezone_by_user_id(con, user_id)
            if timezone is None:
                await send_timezone_reminder_message(bot, chat_id)
                return

    except sqlite3.Error as e:
        logging.error(f"Get timezone failed: {e}")
        raise Exception(e)

    try:
        dt = get_datetime(context)
    except ValueError:
        await send_message(
                bot,
                chat_id,
                "The reminder format is incorrect. Please refert to /help"
        )
        return

    dt = dt.replace(tzinfo=ZoneInfo(timezone))


    job_queue = context.job_queue
    if not job_queue:
        raise Exception("Job queue not avialable")

    data = get_notification_message(context)

    await send_acquire_reminder_message(bot, chat_id, dt)

    job_queue.run_once(callback_reminder, dt, data=data, chat_id=chat_id)
