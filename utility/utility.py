import logging

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from telegram import Update
from telegram.ext import ContextTypes


def get_chat_id(update: Update) -> int:
    if update.message:
        return update.message.chat_id

    logging.error("Update does not contain a valid chat id")  
    raise AttributeError("Update does not contain a valid chat id")


def get_user_id(update: Update) -> str:
    if update.message and update.message.from_user:
        return str(update.message.from_user.id)

    logging.error("Update does not contain valid user id")
    raise AttributeError("Update does not contain valid user id")

def get_seconds(time: int, measure: str) -> int:

    match measure:
        case 's' | 'с':
            return time

        case 'm' | 'м':
            return time * 60

        case 'h' | 'ч':
            return time * 60 * 60

        case 'd' | 'д':
            return time * 60 * 60 * 24

        case _:
            logging.error(f"Invalid measure")
            raise ValueError(
                    "The timer measurement must be 's', 'm', 'h', or 'd'"
            )


def get_timer_seconds(context: ContextTypes.DEFAULT_TYPE) -> int:
    if not context.args:
        raise AttributeError("Time duration is not provided")

    time_str = context.args[0][:len(context.args[0]) - 1]
    measure = context.args[0][-1]

    try:
        time = int(time_str)
    except ValueError:
        logging.exception("Time must be a number")
        raise ValueError("Time must be a number")

    seconds = get_seconds(time, measure) 

    return seconds


def try_parse_datetime(input: str, format: str) -> bool:
    try:
        datetime.strptime(input, format)
        return True
    except ValueError:
        return False


def get_datetime(context: ContextTypes.DEFAULT_TYPE) -> datetime:
    if not context.args:
        logging.error("Date or Time is not provided")
        raise AttributeError("Date or Time is not provided")

    datetime_str = context.args[0]

    match datetime_str:
        case time if try_parse_datetime(time, "%H:%M"):
            now = datetime.now()
            parsed_time = datetime.strptime(time, "%H:%M").time()
            reminder_datetime = now.replace(
                    hour=parsed_time.hour,
                    minute=parsed_time.minute,
                    second=parsed_time.second,
            )
            return reminder_datetime

        case full if try_parse_datetime(full, "%d/%m/%y %H:%M:%S"):
            return datetime.strptime(time, "%d/%m/%y %H:%M:%S")

        case _:
            logging.error("Wrong /remind format")
            raise ValueError("The /remind format is incorrect")


def get_timezone(context: ContextTypes.DEFAULT_TYPE) -> str:
    if not context.args:
        logging.error("Timezone is not provided")
        raise AttributeError("Timezone is not provided")

    timezone = context.args[0]
    
    try:
        ZoneInfo(timezone)
        return timezone
    except ZoneInfoNotFoundError:
        logging.exception("Cannot find this timezone")
        raise ZoneInfoNotFoundError("Cannot find this timezone")


def get_notification_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    if context.args and len(context.args) >= 2:
        return {"text": context.args[1:]}
    return {}

