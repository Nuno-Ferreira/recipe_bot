import logging

from numpy import lookfor

import telegram
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)

from nellie import config
from nellie import exceptions
from nellie import spoonacular_helper as sp


spoon = sp.SpoonacularFacade()

logging.info("Creating updaters and dispatchers...")

UPDATER = Updater(token=config.TELEGRAM_TOKEN)
DISPATCHER = UPDATER.dispatcher

logging.info("Updater and Dispatcher created.")

def format_message_and_get_parse_mode(recipe):
    logging.info("Formatting...")
    parse_mode = telegram.ParseMode.HTML
    message = sp.SpoonacularFacade.format_recipe_data_as_html(recipe)

    if len(message) > config.TELEGRAM_MESSAGE_CHAR_LIMIT:
        logging.info("Recipe too long!")
        link = sp.SpoonacularFacade.format_recipe_title_link_as_markdown(recipe)
        message = (
            f"This recipe was too long to send here\! Here's the "
            f"link instead: {link}"
        )
        parse_mode = telegram.ParseMode.MARKDOWN_V2

    return message, parse_mode


