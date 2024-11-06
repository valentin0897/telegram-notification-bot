import logging

from setup import create_app 


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
)

if __name__ == '__main__':
    application = create_app()

    logging.info("Start polling...")
    application.run_polling()
