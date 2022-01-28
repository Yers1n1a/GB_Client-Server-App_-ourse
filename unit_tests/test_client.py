"""Unit-тесты клиента"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import *
from client import *

class TestClass(unittest.TestCase):

    def test_def_presense(self):
        """Тест коректного запроса"""
        test = create_presence()
        test[TIME] = 1.1  # время необходимо приравнять принудительно
                          # иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        """Тест корректтного разбора ответа 200"""
        self.assertEqual(process_server_answer({RESPONSE: 200, ALERT: 'check'}), '200 : OK, check')

    def test_400_ans(self):
        """Тест корректного разбора 400"""
        self.assertEqual(process_server_answer({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_402_ans(self):
        """Тест корректного разбора 400"""
        self.assertEqual(process_server_answer({RESPONSE: 402, ERROR: 'Bad Request'}), '402 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, process_server_answer, {ERROR: 'Bad Request'})

    def test_auth(self):
        """Тест аутентификации"""
        check_auch = auth('Guest', 'password')
        check_auch[TIME] = 1.1
        self.assertEqual(check_auch,
                         {ACTION: AUTHENTICATE,
                          TIME: 1.1,
                          USER: {ACCOUNT_NAME: 'Guest',
                                 PASSWORD: 'password'}})

    def test_quit(self):
        """Тест выхода с сервера"""
        check_quit = quit_from_server('Guest')
        check_quit[TIME] = 1.1
        self.assertEqual(check_quit,
                         {ACTION: QUIT,
                          TIME: 1.1,
                          USER: {ACCOUNT_NAME: 'Guest'}})


if __name__ == '__main__':
    unittest.main()

#