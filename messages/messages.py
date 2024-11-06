import logging
from datetime import datetime

from telegram import Bot


async def send_message(bot: Bot, chat_id: int, text: str):
    logging.info(f"The message was sent to {chat_id}")
    await bot.send_message(
            chat_id=chat_id,
            text=text
    )


async def send_acquire_timer_message(bot: Bot, chat_id: int, time: str):
    timer_set_text = f"Timer has been set on {time} seconds"
    await send_message(bot, chat_id, timer_set_text)


async def send_acquire_reminder_message(bot: Bot, chat_id: int, dt: datetime):
    dt_str = dt.strftime("%d/%m/%Y %H:%M")
    reminder_set_text = f"Reminder has been set on {dt_str}"
    await send_message(bot, chat_id, reminder_set_text)


async def send_acquire_timezone_message(bot: Bot, chat_id: int, timezone: str):
    set_timezone_set_text = f"Timezone has been set on {timezone}"
    await send_message(bot, chat_id, set_timezone_set_text)


async def send_timezone_reminder_message(bot: Bot, chat_id: int):
    set_settimezone_reminder_text = f"Please, use /settimezone command"
    await send_message(bot, chat_id, set_settimezone_reminder_text)
