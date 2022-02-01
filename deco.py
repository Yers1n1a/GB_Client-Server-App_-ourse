import sys
import logging
import logs.config_server_log
import logs.config_client_log
import traceback
import inspect
import os

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    def wrapper(*args, **kwargs):
        LOGGER.info(f'Функция {func.__name__} вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}.')
        return func(*args, **kwargs)
    return wrapper
