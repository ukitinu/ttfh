"""
Some useful constants and logging config
"""

import logging.handlers
import os

# global constants

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
INI_FILE = os.path.join(os.path.dirname(__file__), 'ttfh.ini')

# logging

if not os.path.exists('./logs'):
    os.mkdir('./logs')

file_handler = logging.handlers.RotatingFileHandler(
    filename='./logs/ttfh.log',
    maxBytes=1024 * 1000 * 4,
    backupCount=10,
    encoding='UTF-8')

file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)-28s - %(levelname)-8s - %(message)s'))

logging.basicConfig(handlers=[file_handler], force=True, level=logging.INFO)
