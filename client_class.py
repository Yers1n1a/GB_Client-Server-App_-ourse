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


class Client(object):
    def __init__(self, account_name,  password):
        self.account_name = account_name
        self.password = password
        self.server_address = DEFAULT_IP_ADDRESS
        self.server_port = DEFAULT_PORT

        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.connect((self.server_address, self.server_port))

    def send_and_listen(self, out):
        send_message(self.transport, out)
        try:
            answer = self.process_server_answer(get_message(self.transport))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print('Не удалось декодировать сообщение сервера.')

    @log
    def process_server_answer(self, message):
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
    def presence(self):
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
                ACCOUNT_NAME: self.account_name
            }
        }
        self.send_and_listen(out)

    @log
    def auth(self):
        out = {
            ACTION: AUTHENTICATE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name,
                PASSWORD: self.password
            }
        }
        self.send_and_listen(out)

    @log
    def quit(self):
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
                ACCOUNT_NAME: self.account_name
            }
        }
        LOGGER.info(f'quit from server at {time.time()}')
        self.send_and_listen(out)

    def send(self, message):
        out = {
            ACTION: MSG,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name
            },
            TO: 'chat',
            FROM: self.account_name,
            MESSAGE: message
        }
        self.send_and_listen(out)


def main():
    client_id = input('Enter your ID and password').split()
    client1 = Client(*client_id)  # на данный момент верные Guest password
    client1.presence()
    client1.auth()
    while True:
        from_input = input('Enter your message or "quit"')
        if from_input == 'quit':
            client1.quit()
            break
        else:
            client1.send(from_input)


if __name__ == '__main__':
    main()


# client1 = Client('Guest', 'password')

# client2 = Client('GOD', 'bella')
# print(client2.auth())


# class ClientSocket(object):
#     __slots__ = ('AF_INET',  'SOCK_STREAM')
#
#     def __init__(self):
#         self.AF_INET = socket.AF_INET
#         self.SOCK_STREAM = socket.SOCK_STREAM
#
#     def start(self):
#         return socket.socket(self.AF_INET, self.SOCK_STREAM)



# @log
# def create_presence(account_name='Guest'):
#     '''
#     Функция генерирует запрос о присутствии клиента
#     :param account_name:
#     :return:
#     '''
#     # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
#     out = {
#         ACTION: PRESENCE,
#         TIME: time.time(),
#         USER: {
#             ACCOUNT_NAME: account_name
#         }
#     }
#     LOGGER.info(f'presence created at {time.time()}')
#     return out
#
# @log
# def process_server_answer(message):
#     '''
#     Функция разбирает ответ сервера
#     :param message:
#     :return:
#     '''
#     if RESPONSE in message:
#         if message[RESPONSE] == 200:
#             return f'200 : OK, {message[ALERT]}'
#         return f'{message[RESPONSE]} : {message[ERROR]}'
#     LOGGER.critical("Can't process server's answer")
#     raise ValueError
#
#
# @log
# def quit_from_server(account_name='Guest'):
#     '''
#     Функция генерирует запрос на выход с сервера
#     :param account_name:
#     :return:
#     '''
#     # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
#     out = {
#         ACTION: QUIT,
#         TIME: time.time(),
#         USER: {
#             ACCOUNT_NAME: account_name
#         }
#     }
#     LOGGER.info(f'quit from server at {time.time()}')
#     return out
#
#
# @log
# def auth(account_name='Guest', password='password'):
#     '''
#     Функция генерирует запрос на аутентификацию клиента
#     :param account_name:
#     :return:
#     '''
#     # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest',
#     # 'password': 'password'}}
#     out = {
#         ACTION: AUTHENTICATE,
#         TIME: time.time(),
#         USER: {
#             ACCOUNT_NAME: account_name,
#             PASSWORD: password
#         }
#     }
#     LOGGER.info(f'auth at {time.time()}')
#     return out
#
#
# def main():
#     '''Загружаем параметы коммандной строки'''
#     # client.py 192.168.1.2 8079
#     try:
#         server_address = sys.argv[1]
#         server_port = int(sys.argv[2])
#         if server_port < 1024 or server_port > 65535:
#             raise ValueError
#         LOGGER.info('Адрес и порт сервера указаны верно')
#     except IndexError:
#         LOGGER.info(f'Used default IP and PORT settings')
#         server_address = DEFAULT_IP_ADDRESS
#         server_port = DEFAULT_PORT
#     except ValueError:
#         LOGGER.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
#         print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
#         sys.exit(1)
#
#     # Инициализация сокета и обмен
#
#     transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     transport.connect((server_address, server_port))
#
#     send_message(transport, create_presence())
#     try:
#         answer = process_server_answer(get_message(transport))
#         print(answer)
#     except (ValueError, json.JSONDecodeError):
#         LOGGER.error('Не удалось декодировать сообщение сервера на этапе присутствия.')
#         print('Не удалось декодировать сообщение сервера.')
#
#     send_message(transport, auth())
#     try:
#         answer = process_server_answer(get_message(transport))
#         print(answer)
#     except (ValueError, json.JSONDecodeError):
#         LOGGER.error('Не удалось декодировать сообщение сервера на этапе авторизации.')
#         print('Не удалось декодировать сообщение сервера.')
#
#     send_message(transport, quit_from_server())
#     try:
#         answer = process_server_answer(get_message(transport))
#         print(answer)
#     except (ValueError, json.JSONDecodeError):
#         LOGGER.error('Не удалось декодировать сообщение сервера на этапе выхода.')
#         print('Не удалось декодировать сообщение сервера.')


# if __name__ == '__main__':
#     main()
