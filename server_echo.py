"""Программа-сервер"""

import socket
import sys
import json
from common.variables import *
from common.utils import *
import logging
import logs.config_server_log
import time
from deco import log
import argparse
import select

LOGGER = logging.getLogger('server')


def process_client_message(message):
    try:
        check = message[ACTION]
        check = message[USER]
    except KeyError:
        return {
                RESPONSE: 400,
                ERROR: f'Bad Request, check required fields'
            }
    if TIME in message:
        if message[ACTION] == PRESENCE:
            if message[USER][ACCOUNT_NAME] == 'Guest':
                return {RESPONSE: 200,
                        ALERT: 'Вы успешно подключились к серверу'}
            else:
                return {RESPONSE: 402,
                        ERROR: 'This could be wrong password or no account with that name'}
        elif message[ACTION] == QUIT:
            return {RESPONSE: 200,
                    ALERT: 'Вы успешно отключены от сервера'}
        elif message[ACTION] == AUTHENTICATE:
            check_auth = ['USER NAME', message[USER][ACCOUNT_NAME] == 'Guest',
                          'PASSWORD', message[USER][PASSWORD] == 'password']
            if all(check_auth):
                return {RESPONSE: 200,
                        ALERT: 'Вы успешно авторизовались'}
            else:
                return {
                    RESPONSE: 402,
                    ERROR: f'This could be wrong password or no account with that name'
                }
        elif message[ACTION] == MSG:
            check_message_text = ['MESSAGE', MESSAGE_TEXT in message]
            if all(check_message_text):
                return {RESPONSE: 200,
                        ALERT: f'Вы прислали сообщение {message[MESSAGE_TEXT]}'}
    else:
        return {
            RESPONSE: 400,
            ERROR: f'Bad Request, check Time'
        }

@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    '''

    LOGGER.info(f'server started at {time.time()}')

    listen_address, listen_port = arg_parser()
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)
    clients = []
    messages = []

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MSG,
                FROM: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


        # message_from_client = get_message(client)
        # # print(message_from_client)
        # response = process_client_message(message_from_client)
        # # print(response)
        # send_message(client, response)
        # # print(message_from_client[ACTION])
        # if response['response'] != 200:
        #     client.close()
        #     client, client_address = transport.accept()
        # if message_from_client[ACTION] == 'quit':
        #     client.close()
        #     client, client_address = transport.accept()


if __name__ == '__main__':
    main()
