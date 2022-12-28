import logging
import os
import pathlib
import sys
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

from pymon import VERSION, bot

if __name__ == '__main__':
    # Setup handler
    log_path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)), "logs")
    log_path.mkdir(exist_ok=True, parents=True)
    log_path = log_path / "pymon.log"
    file_handler = RotatingFileHandler(
        log_path,
        backupCount=10,
        maxBytes=1000000
    )
    console_handler = logging.StreamHandler(sys.stdout)

    # Setup formatter
    msg_format = f'[Pymon {VERSION}] %(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    date_format = '%Y-%m-%d:%H:%M:%S'

    # Setup root logger
    logging.basicConfig(
        handlers=[file_handler, console_handler],
        level=logging.DEBUG,
        format=msg_format,
        datefmt=date_format,
    )

    # Load key environment variables
    load_dotenv()

    # Initialize and run discord bot
    client = bot.Pymon()
    client.run(os.environ.get("DISCORD_TOKEN"), log_handler=None)
