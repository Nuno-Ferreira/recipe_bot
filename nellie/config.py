import os
import logging

LOGFILE = os.environ.get("LOGFILE", "/tmp/nellie.log")

logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_MESSAGE_CHAR_LIMIT = 4096

SPOONACULAR_KEY = os.environ.get("SPOONACULAR_KEY")
RECIPE_LIMIT = 3
ALLOWED_TAGS = [
    
]