import logging

from telegram.ext import ApplicationBuilder, Application, CommandHandler

from handlers import timer, reminder, set_timezone
from db import connect_db, create_db
from config import Config

def init_db() -> None:
    with connect_db() as con:
        create_db(con)

    logging.info("Database initialized successfuly...")


def create_app() -> Application:
    token = Config.TELEGRAM_BOT_TOKEN

    init_db()

    if token is None:
        raise EnvironmentError(
            "Required environment variable 'TELEGRAM_BOT_TOKEN is not set'"
        )

    builder = ApplicationBuilder()
    builder.token(token)
    app = builder.build()

    app = setup_handlers(app)

    logging.info("Application initialized")

    return app


def setup_handlers(app: Application) -> Application:
    timer_handler = CommandHandler('timer', timer)
    reminder_handler = CommandHandler('remind', reminder)
    set_timezone_handler = CommandHandler('timezone', set_timezone)

    app.add_handler(timer_handler)
    app.add_handler(reminder_handler)
    app.add_handler(set_timezone_handler)

    return app

