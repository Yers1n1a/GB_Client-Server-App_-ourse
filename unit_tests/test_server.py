"""Unit-тесты сервера"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import *
from server import *

class TestServer(unittest.TestCase):
    '''
    В сервере только 1 функция для тестирования
    '''
    def setUp(self):
        self.err_dict = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        self.ok_dict = {
            RESPONSE: 200,
            ALERT: ''
        }

    def test_presence_no_action(self):
        """Ошибка если нет действия"""
        self.err_dict[ERROR] = 'Bad Request, check required fields'
        self.assertEqual(check_client_presence(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_quit_no_action(self):
        """Ошибка если нет действия"""
        self.err_dict[ERROR] = 'Bad Request, check required fields'
        self.assertEqual(check_client_quit(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_auth_no_action(self):
        """Ошибка если нет действия"""
        self.err_dict[ERROR] = 'Bad Request, check required fields'
        self.assertEqual(check_client_auth(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_presence_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.err_dict[ERROR] = 'Bad Request, check ACTION_TYPE'
        self.assertEqual(check_client_presence(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_quit_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.err_dict[ERROR] = 'Bad Request, check ACTION_TYPE'
        self.assertEqual(check_client_quit(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_auth_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.err_dict[ERROR] = 'Bad Request, check ACTION_TYPE'
        self.assertEqual(check_client_auth(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest', PASSWORD: 'password'}}), self.err_dict)

    def test_presence_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.err_dict[ERROR] = 'Bad Request, check TIME'
        self.assertEqual(check_client_presence(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_quit_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.err_dict[ERROR] = 'Bad Request, check TIME'
        self.assertEqual(check_client_quit(
            {ACTION: QUIT, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_auth_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.err_dict[ERROR] = 'Bad Request, check TIME'
        self.assertEqual(check_client_auth(
            {ACTION: AUTHENTICATE, USER: {ACCOUNT_NAME: 'Guest', PASSWORD: 'password'}}), self.err_dict)

    def test_presence_no_user(self):
        """Ошибка - нет пользователя"""
        self.err_dict[ERROR] = 'Bad Request, check required fields'
        self.assertEqual(check_client_presence(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_quit_no_user(self):
        """Ошибка - нет пользователя"""
        self.err_dict[ERROR] = 'Bad Request, check required fields'
        self.assertEqual(check_client_quit(
            {ACTION: QUIT, TIME: '1.1'}), self.err_dict)

    def test_auth_no_user(self):
        """Ошибка - нет пользователя"""
        self.err_dict[ERROR] = 'Bad Request, check required fields'
        self.assertEqual(check_client_auth(
            {ACTION: AUTHENTICATE, TIME: '1.1'}), self.err_dict)

    def test_presence_unknown_user(self):
        """Ошибка - не Guest"""
        self.err_dict[ERROR] = 'Bad Request, check USER NAME'
        self.assertEqual(check_client_presence(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_quit_unknown_user(self):
        self.err_dict[ERROR] = 'Bad Request, check USER NAME'
        self.assertEqual(check_client_quit(
            {ACTION: QUIT, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_auth_unknown_user(self):
        self.err_dict[RESPONSE] = 402
        self.err_dict[ERROR] = 'This could be wrong password or no account with that name'
        self.assertEqual(check_client_auth(
            {ACTION: AUTHENTICATE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1', PASSWORD: 'password'}}), self.err_dict)

    def test_ok_check_presence(self):
        """Корректный запрос на присутствие"""
        self.ok_dict[ALERT] = 'Вы успешно подключились к серверу'
        self.assertEqual(check_client_presence(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

    def test_ok_check_quit(self):
        """Корректный запрос на выход с сервера"""
        self.ok_dict[ALERT] = 'Вы успешно отключены от сервера'
        self.assertEqual(check_client_quit(
            {ACTION: QUIT, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

    def test_ok_check_auth(self):
        """Корректный запрос на аутентификацию"""
        self.ok_dict[ALERT] = 'Вы успешно авторизовались'
        self.assertEqual(check_client_auth(
            {ACTION: AUTHENTICATE, TIME: 1.1,
             USER: {ACCOUNT_NAME: 'Guest', PASSWORD: 'password'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
