import logging

from telegram import Update
from telegram.ext import ContextTypes

from messages import send_message, send_acquire_timer_message 
from utility import get_chat_id, get_timer_seconds, get_notification_message


async def callback_timer(context: ContextTypes.DEFAULT_TYPE):
    if context.job is not None and context.job.chat_id is not None:
        chat_id = context.job.chat_id
        bot = context.bot
        data = context.job.data
        if isinstance(data, dict):
            text = data["text"]
        else:
            text = "Alarm"

        await send_message(bot, chat_id, text)
    else:
        raise Exception("There is no job attached to this callback")


async def timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat_id = get_chat_id(update)

    try:
        seconds = get_timer_seconds(context)
    except ValueError:
        await send_message(
                bot,
                chat_id,
                "The timer message format is incorrect. Plear refer to /help"
        )
        return

    job_queue = context.job_queue
    if not job_queue:
        raise Exception("Job queue not available")

    data = get_notification_message(context)

    await send_acquire_timer_message(bot, chat_id, str(seconds))

    job_queue.run_once(callback_timer, seconds, data=data, chat_id=chat_id)
