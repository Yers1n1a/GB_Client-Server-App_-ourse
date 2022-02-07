"""Константы"""
import logging

# Порт по умолчанию для сетевого ваимодействия

DEFAULT_PORT = 7778
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 1
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Уровень фиксации логов
LOGGING_LEVEL = logging.INFO

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PASSWORD = 'password'
FROM = 'from'
TO = 'to'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
QUIT = 'quit'
ALERT = 'alert'
AUTHENTICATE = 'authenticate'
MSG = 'send message to chat or user'
MESSAGE_TEXT = 'Message: '

