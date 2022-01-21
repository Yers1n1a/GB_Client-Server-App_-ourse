"""Программа-сервер"""

import socket
import sys
import json
from common.variables import *
from common.utils import *


def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    check_message = ['ACTION', ACTION in message,
                     'PRESENCE', message[ACTION] == PRESENCE,
                     'TIME', TIME in message,
                     'USER', USER in message,
                     'USER NAME', message[USER][ACCOUNT_NAME] == 'Guest']
    if all(check_message):
        return {RESPONSE: 200,
                ALERT: 'Вы успешно подключились к серверу'}
    else:
        return {
                RESPONSE: 400,
                ERROR: f'Bad Request, check {check_message[check_message.index(False)-1]}'
            }


def check_client_quit(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента и отключает его
    от сервера

    :param message:
    :return:
    '''
    check_message = ['ACTION', ACTION in message,
                     'QUIT', message[ACTION] == QUIT,
                     'TIME', TIME in message,
                     'USER', USER in message,
                     'USER NAME', message[USER][ACCOUNT_NAME] == 'Guest']
    if all(check_message):
        return {RESPONSE: 200,
                ALERT: 'Вы успешно отключены от сервера'}
    else:
        return {
                RESPONSE: 400,
                ERROR: f'Bad Request, waiting for QUIT'
            }


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    '''

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if 65535 < listen_port < 1024:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_cient)
            send_message(client, response)
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()

        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = check_client_quit(message_from_cient)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
