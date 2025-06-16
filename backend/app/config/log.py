from loguru import logger
from pathlib import Path
import os

LOG_PATH = Path(os.path.join('storage', 'logs'))
LOG_FILE = LOG_PATH / 'app.log'

def setup_logger() -> None:
    """
    Setup the logger for the application.
    """
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    logger.remove()
    
    level = 'INFO' if os.getenv('APP_ENV') == 'production' else 'DEBUG'
    logger.add(LOG_FILE, rotation='10MB', retention='1 year', level=level, encoding='utf-8')
    
    if os.getenv('APP_ENV') != 'production':
        logger.add(lambda msg: print(msg, end=''), level='DEBUG')




