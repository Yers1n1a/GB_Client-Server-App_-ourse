"""Программа-клиент"""

import sys
import json
import socket
import time
from common.variables import *
from common.utils import *
import logging
import logs.config_client_log
from deco import log

LOGGER = logging.getLogger('client')


@log
def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER.info(f'presence created at {time.time()}')
    return out

@log
def process_server_answer(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return f'200 : OK, {message[ALERT]}'
        return f'{message[RESPONSE]} : {message[ERROR]}'
    LOGGER.critical("Can't process server's answer")
    raise ValueError


@log
def quit_from_server(account_name='Guest'):
    '''
    Функция генерирует запрос на выход с сервера
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: QUIT,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER.info(f'quit from server at {time.time()}')
    return out


@log
def auth(account_name='Guest', password='password'):
    '''
    Функция генерирует запрос на аутентификацию клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest',
    # 'password': 'password'}}
    out = {
        ACTION: AUTHENTICATE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            PASSWORD: password
        }
    }
    LOGGER.info(f'auth at {time.time()}')
    return out


def main():
    '''Загружаем параметы коммандной строки'''
    # client.py 192.168.1.2 8079
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
        LOGGER.info('Адрес и порт сервера указаны верно')
    except IndexError:
        LOGGER.info(f'Used default IP and PORT settings')
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        LOGGER.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))

    send_message(transport, create_presence())
    try:
        answer = process_server_answer(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        LOGGER.error('Не удалось декодировать сообщение сервера на этапе присутствия.')
        print('Не удалось декодировать сообщение сервера.')

    send_message(transport, auth())
    try:
        answer = process_server_answer(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        LOGGER.error('Не удалось декодировать сообщение сервера на этапе авторизации.')
        print('Не удалось декодировать сообщение сервера.')

    send_message(transport, quit_from_server())
    try:
        answer = process_server_answer(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        LOGGER.error('Не удалось декодировать сообщение сервера на этапе выхода.')
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
